"""
Script para analisar o impacto da migração de cada módulo.
"""

import ast
import os
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Mapeamento de migrações
MIGRATIONS = {
    'agents': {
        'from': 'agents',
        'to': 'core/agents',
        'import_old': 'agents.',
        'import_new': 'core.agents.',
    },
    'utils': {
        'from': 'utils',
        'to': 'core/utils',
        'import_old': 'utils.',
        'import_new': 'core.utils.',
    },
    'app': {
        'from': 'app',
        'to': 'products/revelar/app',
        'import_old': 'app.',
        'import_new': 'products.revelar.app.',
    },
    'cli': {
        'from': 'cli',
        'to': 'core/tools/cli',
        'import_old': 'cli.',
        'import_new': 'core.tools.cli.',
    },
    'tests': {
        'from': 'tests',
        'to': 'tests/core',
        'import_old': None,  # Testes importam outros módulos, não são importados
        'import_new': None,
    },
    'docs': {
        'from': 'docs',
        'to': 'docs/core',
        'import_old': None,  # Docs não têm imports Python
        'import_new': None,
    },
}


def get_python_files(root_dir: str = '.') -> List[Path]:
    """Retorna lista de todos os arquivos Python do projeto."""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    return python_files


def get_markdown_files(root_dir: str = '.') -> List[Path]:
    """Retorna lista de todos os arquivos Markdown do projeto."""
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files


def count_files_in_directory(directory: str) -> Tuple[int, int, int, List[str]]:
    """Conta arquivos em um diretório e retorna (total, código, testes, docs, lista)."""
    path = Path(directory)
    if not path.exists():
        return 0, 0, 0, []
    
    code_count = 0
    test_count = 0
    doc_count = 0
    files = []
    
    for root, dirs, filenames in os.walk(path):
        if '__pycache__' in root:
            continue
        for filename in filenames:
            files.append(filename)
            if filename.endswith('.py'):
                if 'test' in filename.lower() or 'test' in root.lower():
                    test_count += 1
                else:
                    code_count += 1
            elif filename.endswith('.md'):
                doc_count += 1
    
    total = len(files)
    return total, code_count, test_count, doc_count


def extract_imports_affected(file_path: Path, import_pattern: str) -> Tuple[int, List[str]]:
    """
    Extrai imports que serão afetados pela migração.
    Retorna: (contagem, lista de imports)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        
        affected_imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(import_pattern):
                        affected_imports.append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith(import_pattern):
                    affected_imports.append(node.module)
        
        return len(affected_imports), affected_imports
    
    except Exception as e:
        return 0, []


def count_affected_files(migration: Dict, python_files: List[Path]) -> Dict:
    """Conta arquivos afetados por uma migração."""
    import_pattern = migration['import_old']
    if not import_pattern:
        return {
            'files_affected': 0,
            'imports_to_adjust': 0,
            'affected_imports_list': []
        }
    
    files_affected = 0
    total_imports = 0
    all_affected_imports = []
    
    for file_path in python_files:
        count, imports = extract_imports_affected(file_path, import_pattern)
        if count > 0:
            files_affected += 1
            total_imports += count
            all_affected_imports.extend(imports)
    
    return {
        'files_affected': files_affected,
        'imports_to_adjust': total_imports,
        'affected_imports_list': all_affected_imports
    }


def count_doc_references(migration: Dict, md_files: List[Path]) -> Dict:
    """Conta referências em documentação Markdown."""
    from_pattern = migration['from']
    to_pattern = migration['to'].replace('/', '/')
    
    references = 0
    affected_files = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Busca padrões comuns em docs
            patterns = [
                f'{from_pattern}/',
                f'`{from_pattern}/',
                f'[{from_pattern}/',
                f'({from_pattern}/',
            ]
            
            file_refs = 0
            for pattern in patterns:
                file_refs += content.count(pattern)
            
            if file_refs > 0:
                references += file_refs
                affected_files.append((str(md_file), file_refs))
        
        except Exception:
            pass
    
    return {
        'references': references,
        'affected_files': affected_files
    }


def estimate_risk(migration: Dict, impact_data: Dict) -> Tuple[str, str]:
    """Estima risco de quebra baseado em métricas."""
    files_affected = impact_data.get('files_affected', 0)
    imports_to_adjust = impact_data.get('imports_to_adjust', 0)
    
    # Critérios de risco
    if files_affected > 50 or imports_to_adjust > 100:
        risk = 'Alto'
        reason = f'Muitos arquivos afetados ({files_affected}) e muitos imports a ajustar ({imports_to_adjust}). Requer atenção cuidadosa e testes extensivos.'
    elif files_affected > 20 or imports_to_adjust > 50:
        risk = 'Médio'
        reason = f'Quantidade moderada de arquivos ({files_affected}) e imports ({imports_to_adjust}). Requer testes após migração.'
    else:
        risk = 'Baixo'
        reason = f'Poucos arquivos afetados ({files_affected}) e imports ({imports_to_adjust}). Migração relativamente simples.'
    
    return risk, reason


def estimate_time(migration: Dict, impact_data: Dict, doc_data: Dict, file_counts: Dict) -> str:
    """Estima tempo de migração em horas."""
    files_affected = impact_data.get('files_affected', 0)
    imports_to_adjust = impact_data.get('imports_to_adjust', 0)
    doc_references = doc_data.get('references', 0)
    code_files = file_counts.get('code_files', 0)
    
    # Estimativa baseada em experiência (mais realista)
    # - Mover arquivos: ~5 minutos (git mv é rápido)
    # - Ajustar imports: ~1 minuto por arquivo afetado (busca/substituição)
    # - Ajustar docs: ~30 segundos por 10 referências (busca/substituição)
    # - Testes e validação: ~30 minutos por módulo
    
    move_time = 0.08  # ~5 minutos para mover estrutura
    import_time = files_affected * 0.017  # ~1 minuto por arquivo (busca/substituição)
    doc_time = doc_references * 0.005  # ~30 segundos por 10 referências
    test_time = 0.5  # 30 minutos para testar
    
    total_hours = (move_time + import_time + doc_time + test_time)
    
    if total_hours < 1:
        return f"{int(total_hours * 60)} minutos"
    elif total_hours < 2:
        return f"{total_hours:.1f} horas"
    else:
        return f"{int(total_hours)} horas"


def analyze_migration(migration_name: str, migration: Dict) -> Dict:
    """Analisa impacto de uma migração específica."""
    print(f"Analisando migração: {migration_name}...")
    
    # Conta arquivos no diretório de origem
    source_dir = migration['from']
    file_count, code_count, test_count, doc_count = count_files_in_directory(source_dir)
    
    # Analisa imports afetados
    python_files = get_python_files()
    impact_data = count_affected_files(migration, python_files)
    
    # Analisa referências em docs
    md_files = get_markdown_files()
    doc_data = count_doc_references(migration, md_files)
    
    # Estima risco
    risk, risk_reason = estimate_risk(migration, impact_data)
    
    # Estima tempo
    file_counts = {
        'code_files': code_count,
        'test_files': test_count,
        'doc_files': doc_count,
    }
    time_estimate = estimate_time(migration, impact_data, doc_data, file_counts)
    
    return {
        'migration_name': migration_name,
        'source_dir': source_dir,
        'target_dir': migration['to'],
        'file_count': file_count,
        'code_files': code_count,
        'test_files': test_count,
        'doc_files': doc_count,
        'files_affected': impact_data['files_affected'],
        'imports_to_adjust': impact_data['imports_to_adjust'],
        'doc_references': doc_data['references'],
        'risk': risk,
        'risk_reason': risk_reason,
        'time_estimate': time_estimate,
    }


def generate_report(analyses: List[Dict]) -> str:
    """Gera relatório em Markdown."""
    report = []
    report.append("# Análise de Impacto da Migração\n")
    report.append("Estimativas detalhadas do impacto de mover cada módulo principal.\n")
    
    for analysis in analyses:
        name = analysis['migration_name'].upper()
        report.append(f"## {analysis['migration_name']}/ → {analysis['target_dir']}/\n")
        
        report.append("### Arquivos Afetados\n")
        report.append(f"- **Arquivos de código**: {analysis['code_files']} arquivos")
        report.append(f"- **Arquivos de testes**: {analysis['test_files']} arquivos")
        report.append(f"- **Arquivos de documentação**: {analysis['doc_files']} arquivos")
        report.append(f"- **Total de arquivos no diretório**: {analysis['file_count']} arquivos\n")
        
        report.append("### Imports a Ajustar\n")
        if analysis['imports_to_adjust'] > 0:
            report.append(f"- **Arquivos que precisam ajustar imports**: {analysis['files_affected']} arquivos")
            report.append(f"- **Total de imports a ajustar**: ~{analysis['imports_to_adjust']} linhas")
        else:
            report.append("- **N/A**: Este módulo não é importado por outros (ou não tem imports Python)\n")
        
        report.append("### Referências em Documentação\n")
        if analysis['doc_references'] > 0:
            report.append(f"- **Referências a ajustar**: ~{analysis['doc_references']} referências")
        else:
            report.append("- **N/A**: Nenhuma referência encontrada em documentação\n")
        
        report.append("### Risco de Quebra\n")
        report.append(f"- **Nível**: **{analysis['risk']}**")
        report.append(f"- **Justificativa**: {analysis['risk_reason']}\n")
        
        report.append("### Tempo Estimado de Migração\n")
        report.append(f"- **Estimativa**: {analysis['time_estimate']}\n")
        report.append("")
        report.append("---\n")
        report.append("")
    
    # Resumo geral
    report.append("## Resumo Geral\n")
    report.append("| Módulo | Arquivos | Imports | Docs | Risco | Tempo |")
    report.append("|--------|----------|---------|------|-------|-------|")
    
    total_files = 0
    total_imports = 0
    total_docs = 0
    
    for analysis in analyses:
        total_files += analysis['code_files'] + analysis['test_files']
        total_imports += analysis['imports_to_adjust']
        total_docs += analysis['doc_references']
        
        report.append(
            f"| `{analysis['migration_name']}/` | "
            f"{analysis['code_files'] + analysis['test_files']} | "
            f"{analysis['imports_to_adjust']} | "
            f"{analysis['doc_references']} | "
            f"{analysis['risk']} | "
            f"{analysis['time_estimate']} |"
        )
    
    report.append("")
    report.append(f"**Totais**: {total_files} arquivos, {total_imports} imports, {total_docs} referências em docs\n")
    
    return "\n".join(report)


def main():
    """Função principal."""
    print("Analisando impacto das migrações...")
    
    analyses = []
    for migration_name, migration_config in MIGRATIONS.items():
        analysis = analyze_migration(migration_name, migration_config)
        analyses.append(analysis)
        print(f"  ✅ {migration_name}: {analysis['files_affected']} arquivos afetados")
    
    # Gera relatório
    print("Gerando relatório...")
    report = generate_report(analyses)
    
    # Salva relatório
    output_dir = Path('analysis')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'migration_impact.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Relatório gerado em: {output_file}")


if __name__ == '__main__':
    main()

