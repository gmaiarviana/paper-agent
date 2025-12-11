"""
Script para analisar todos os imports do projeto e gerar relatório de dependências.
"""

import ast
import os
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Diretórios principais do projeto
MAIN_DIRS = ['agents', 'app', 'cli', 'utils', 'tests', 'scripts']


def get_python_files(root_dir: str = '.') -> List[Path]:
    """Retorna lista de todos os arquivos Python do projeto."""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # Ignorar venv e __pycache__
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    return python_files


def normalize_module_path(module_path: str, current_file: Path) -> str:
    """Normaliza caminho do módulo para formato padrão."""
    # Remove extensão .py se houver
    module_path = module_path.replace('.py', '')
    
    # Se é relativo, converte para absoluto
    if module_path.startswith('.'):
        parts = module_path.split('.')
        depth = len([p for p in parts if p == ''])
        
        # Remove pontos iniciais
        module_path = '.'.join([p for p in parts if p])
        
        # Constrói caminho absoluto
        current_parts = current_file.parts
        # Remove nome do arquivo
        current_parts = current_parts[:-1]
        
        # Remove partes conforme profundidade
        if depth > 0:
            current_parts = current_parts[:-(depth-1)] if depth > 1 else current_parts
        
        # Constrói módulo
        if module_path:
            full_path = list(current_parts) + [module_path]
        else:
            full_path = list(current_parts)
        
        # Remove partes vazias e normaliza
        full_path = [p for p in full_path if p and p != '__init__']
        return '.'.join(full_path)
    
    return module_path


def extract_imports(file_path: Path) -> Tuple[List[str], List[str], int]:
    """
    Extrai imports de um arquivo Python.
    Retorna: (imports_absolutos, imports_relativos, total_imports)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        
        absolute_imports = []
        relative_imports = []
        total_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    total_count += 1
                    if alias.name.startswith('.'):
                        relative_imports.append(alias.name)
                    else:
                        absolute_imports.append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    total_count += 1
                    if node.module.startswith('.'):
                        relative_imports.append(node.module)
                    else:
                        absolute_imports.append(node.module)
                else:
                    # from . import something
                    total_count += 1
                    relative_imports.append('.')
        
        return absolute_imports, relative_imports, total_count
    
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return [], [], 0


def get_module_directory(module_path: str) -> str:
    """Retorna o diretório principal do módulo."""
    parts = module_path.split('.')
    if parts and parts[0] in MAIN_DIRS:
        return parts[0]
    return 'other'


def build_dependency_graph(files: List[Path]) -> Dict:
    """Constrói grafo de dependências."""
    dependency_data = {
        'module_imports': Counter(),  # Contador de quantas vezes cada módulo é importado
        'file_imports': {},  # Imports por arquivo
        'directory_deps': defaultdict(lambda: defaultdict(int)),  # Dependências entre diretórios
        'relative_count': 0,
        'absolute_count': 0,
        'file_import_counts': {},  # Total de imports por arquivo
        'all_imports': defaultdict(set),  # Todos os imports de cada arquivo
    }
    
    for file_path in files:
        abs_imports, rel_imports, total = extract_imports(file_path)
        
        file_key = str(file_path).replace('\\', '/')
        dependency_data['file_import_counts'][file_key] = total
        
        # Conta relativos vs absolutos
        dependency_data['relative_count'] += len(rel_imports)
        dependency_data['absolute_count'] += len(abs_imports)
        
        # Processa imports absolutos
        file_dir = get_module_directory(file_key)
        all_file_imports = []
        
        for imp in abs_imports:
            # Normaliza módulo (pega apenas a parte principal)
            module_parts = imp.split('.')
            main_module = module_parts[0] if module_parts else imp
            
            dependency_data['module_imports'][imp] += 1
            
            # Dependências entre diretórios
            imp_dir = get_module_directory(imp)
            if file_dir != imp_dir and imp_dir != 'other':
                dependency_data['directory_deps'][file_dir][imp_dir] += 1
            
            all_file_imports.append(imp)
        
        # Processa imports relativos
        for imp in rel_imports:
            all_file_imports.append(imp)
        
        dependency_data['file_imports'][file_key] = {
            'absolute': abs_imports,
            'relative': rel_imports,
            'total': total
        }
        
        dependency_data['all_imports'][file_key] = set(all_file_imports)
    
    return dependency_data


def detect_circular_dependencies(dependency_data: Dict) -> List[Tuple[str, str]]:
    """Detecta dependências circulares."""
    circular = []
    
    # Constrói grafo direcionado
    graph = defaultdict(set)
    for file_path, imports in dependency_data['all_imports'].items():
        file_module = file_path.replace('\\', '/').replace('.py', '').replace('/', '.')
        for imp in imports:
            if not imp.startswith('.'):
                # Normaliza para comparar
                imp_parts = imp.split('.')
                if imp_parts[0] in MAIN_DIRS:
                    graph[file_module].add(imp)
    
    # Detecta ciclos simples (A -> B -> A)
    for node_a in graph:
        for node_b in graph[node_a]:
            if node_b in graph and node_a in graph[node_b]:
                # Verifica se realmente há ciclo
                if any(a in graph.get(node_b, set()) for a in [node_a] + list(graph[node_a])):
                    circular.append((node_a, node_b))
    
    return circular


def generate_report(dependency_data: Dict, circular: List[Tuple[str, str]]) -> str:
    """Gera relatório em Markdown."""
    report = []
    report.append("# Mapeamento de Dependências (Imports)\n")
    report.append("Análise completa de todos os imports do projeto.\n")
    
    # 1. Hotspots de Importação (Top 20)
    report.append("## 1. Hotspots de Importação (Top 20)\n")
    report.append("Módulos mais importados no projeto:\n")
    report.append("| Módulo | Contagem |")
    report.append("|--------|----------|")
    
    top_modules = dependency_data['module_imports'].most_common(20)
    for module, count in top_modules:
        report.append(f"| `{module}` | {count} |")
    
    report.append("")
    
    # 2. Dependências por Diretório
    report.append("## 2. Dependências por Diretório\n")
    report.append("Análise de imports cruzados entre diretórios principais:\n")
    
    for source_dir in sorted(dependency_data['directory_deps'].keys()):
        deps = dependency_data['directory_deps'][source_dir]
        if deps:
            report.append(f"### `{source_dir}/` importa de:\n")
            report.append("| Diretório | Quantidade |")
            report.append("|-----------|------------|")
            for target_dir, count in sorted(deps.items(), key=lambda x: -x[1]):
                report.append(f"| `{target_dir}/` | {count} |")
            report.append("")
    
    # 3. Dependências Circulares
    report.append("## 3. Dependências Circulares\n")
    if circular:
        report.append("⚠️ **ATENÇÃO**: Foram encontradas dependências circulares:\n")
        report.append("| Módulo A | Módulo B |")
        report.append("|----------|----------|")
        for mod_a, mod_b in circular[:20]:  # Limita a 20 para não ficar muito longo
            report.append(f"| `{mod_a}` | `{mod_b}` |")
        if len(circular) > 20:
            report.append(f"\n*... e mais {len(circular) - 20} dependências circulares*")
    else:
        report.append("✅ **Nenhuma dependência circular detectada.**\n")
    report.append("")
    
    # 4. Imports Relativos vs Absolutos
    report.append("## 4. Imports Relativos vs Absolutos\n")
    total_imports = dependency_data['relative_count'] + dependency_data['absolute_count']
    rel_percent = (dependency_data['relative_count'] / total_imports * 100) if total_imports > 0 else 0
    abs_percent = (dependency_data['absolute_count'] / total_imports * 100) if total_imports > 0 else 0
    
    report.append("| Tipo | Quantidade | Percentual |")
    report.append("|------|------------|------------|")
    report.append(f"| Relativos (`from .`) | {dependency_data['relative_count']} | {rel_percent:.1f}% |")
    report.append(f"| Absolutos (`from agents.`) | {dependency_data['absolute_count']} | {abs_percent:.1f}% |")
    report.append(f"| **Total** | **{total_imports}** | **100%** |")
    report.append("")
    report.append("> ⚠️ **Nota**: Imports relativos podem quebrar após migração de estrutura de diretórios.\n")
    report.append("")
    
    # 5. Arquivos com Mais Imports (Top 10)
    report.append("## 5. Arquivos com Mais Imports (Top 10)\n")
    report.append("Arquivos críticos para migração (maior número de dependências):\n")
    report.append("| Arquivo | Total de Imports |")
    report.append("|---------|------------------|")
    
    top_files = sorted(
        dependency_data['file_import_counts'].items(),
        key=lambda x: -x[1]
    )[:10]
    
    for file_path, count in top_files:
        # Formata caminho para ser mais legível
        display_path = file_path.replace('\\', '/')
        report.append(f"| `{display_path}` | {count} |")
    
    report.append("")
    
    # Estatísticas adicionais
    report.append("## Estatísticas Gerais\n")
    report.append(f"- **Total de arquivos Python analisados**: {len(dependency_data['file_imports'])}\n")
    report.append(f"- **Total de imports únicos**: {len(dependency_data['module_imports'])}\n")
    report.append(f"- **Total de imports (com repetição)**: {sum(dependency_data['module_imports'].values())}\n")
    
    return "\n".join(report)


def main():
    """Função principal."""
    print("Analisando imports do projeto...")
    
    # Encontra todos os arquivos Python
    python_files = get_python_files()
    print(f"Encontrados {len(python_files)} arquivos Python")
    
    # Analisa dependências
    print("Construindo grafo de dependências...")
    dependency_data = build_dependency_graph(python_files)
    
    # Detecta dependências circulares
    print("Detectando dependências circulares...")
    circular = detect_circular_dependencies(dependency_data)
    
    # Gera relatório
    print("Gerando relatório...")
    report = generate_report(dependency_data, circular)
    
    # Salva relatório
    output_dir = Path('analysis')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'dependency_map.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Relatório gerado em: {output_file}")
    print(f"\nResumo:")
    print(f"  - Top módulo importado: {dependency_data['module_imports'].most_common(1)[0]}")
    print(f"  - Dependências circulares: {len(circular)}")
    print(f"  - Imports relativos: {dependency_data['relative_count']}")
    print(f"  - Imports absolutos: {dependency_data['absolute_count']}")


if __name__ == '__main__':
    main()

