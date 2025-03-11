from elasticsearch import Elasticsearch

from src.config import settings


class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(
            f"http://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}",
            basic_auth=("elastic", settings.ELASTIC_PASSWORD)
        )
        self.index_name = 'user_logs'
        self._create_index_if_not_exists()

    def _create_index_if_not_exists(self):
        if not self.es.indices.exists(index=self.index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "level": {"type": "keyword"},
                        "message": {"type": "text"},
                        "user_id": {"type": "integer"}
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=mappings)

    def index_logs(self, logs):
        if not logs:
            return

        bulk_data = []
        for log in logs:
            bulk_data.append({"index": {"_index": self.index_name}})
            bulk_data.append(log)

        return self.es.bulk(body=bulk_data, refresh=True)

    def search_user_logs(self, user_id, start_time=None, end_time=None, keyword=None, level=None):
        must_clauses = [{"term": {"user_id": user_id}}]

        if start_time and end_time:
            range_filter = {"range": {"timestamp": {}}}
            if start_time:
                range_filter["range"]["timestamp"]["gte"] = start_time.isoformat()
            if end_time:
                range_filter["range"]["timestamp"]["lte"] = end_time.isoformat()
            must_clauses.append(range_filter)

        if keyword:
            must_clauses.append({
                "match": {"message": keyword}
            })

        if level:
            must_clauses.append({
                "term": {"level": level.upper()}
            })

        query = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "sort": [{"timestamp": {"order": "asc"}}]
        }

        return self.es.search(index=self.index_name, body=query)