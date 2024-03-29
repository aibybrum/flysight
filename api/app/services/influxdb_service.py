import app.config.influxdb as influxdb

class InfluxDBService:
    def __init__(self):
        self.client = influxdb.client
        self.bucket = influxdb.bucket

    def get_data_frame(self, query):
        response = self.client.query_api().query(query=query)
        data_df = pd.DataFrame(response.records)
        return data_df
        