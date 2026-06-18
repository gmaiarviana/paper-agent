"""Fila reativa da plataforma de workflow.

Detecção determinística de itens de fila a partir do estado-do-mundo
(ROADMAPs parseados + branches do remote). Sem persistência própria —
fila é função pura do estado, reconstruída por render.
"""
