"""Testes unitários para core/agents/writer/models.py — C-ENSAIO-3.1."""

import json

from core.agents.writer.models import Article, Section


class TestSectionModel:
    def test_section_has_required_fields(self):
        section: Section = {"title": "Introdução", "body": "Texto.", "status": "empty"}
        assert section["title"] == "Introdução"
        assert section["body"] == "Texto."
        assert section["status"] == "empty"

    def test_section_serializes_to_json(self):
        section: Section = {"title": "Métodos", "body": "", "status": "draft"}
        dumped = json.dumps(section)
        loaded = json.loads(dumped)
        assert loaded["title"] == "Métodos"
        assert loaded["status"] == "draft"

    def test_all_status_values(self):
        for status in ("empty", "draft", "edited"):
            section: Section = {"title": "X", "body": "", "status": status}
            assert json.dumps(section)  # não lança exceção


class TestArticleType:
    def test_article_is_list_of_sections(self):
        article: Article = [
            {"title": "Introdução", "body": "...", "status": "draft"},
            {"title": "Métodos", "body": "", "status": "empty"},
        ]
        assert len(article) == 2
        assert article[0]["title"] == "Introdução"

    def test_empty_article(self):
        article: Article = []
        assert json.dumps(article) == "[]"

    def test_article_serializes_to_json(self):
        article: Article = [
            {"title": "A", "body": "Corpo A.", "status": "edited"},
            {"title": "B", "body": "Corpo B.", "status": "draft"},
        ]
        dumped = json.dumps(article)
        loaded = json.loads(dumped)
        assert len(loaded) == 2
        assert loaded[0]["title"] == "A"
        assert loaded[1]["status"] == "draft"
