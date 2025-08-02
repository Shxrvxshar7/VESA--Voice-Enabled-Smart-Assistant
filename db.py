import json
import threading
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timezone
from queue import Queue

class PushToMongo:

    def __init__(self, db="vesa_db", col="system_status"):
        self.mongo_uri = "mongodb+srv://llm:llm@alpha1.aul5rqy.mongodb.net/?retryWrites=true&w=majority&appName=Alpha1"
        self.DATABASE_NAME = db
        self.COLLECTION_NAME = col
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.DATABASE_NAME]
        self.collection = self.db[self.COLLECTION_NAME]
        self.queue = Queue()
        #llm
    

    def push_json(self, json_data):
        try:
            json_data['time'] = datetime.now(timezone.utc)
            self.collection.insert_one(json_data)
            print("✅ Inserted 1 document successfully.")
        except Exception as e:
            print("❌ Failed to insert document:", e)

    def watch_for_updates(self):
        """
        Listen for new inserts to the collection and print them in real time.
        """
        print("👀 Watching MongoDB for new inserts...")
        try:
            with self.collection.watch([{"$match": {"operationType": "insert"}}]) as stream:
                for change in stream:
                    #print(json.dumps(change["fullDocument"], indent=2, default=str))
                    document = json.dumps(change["fullDocument"], indent=2, default=str)
                    self.queue.put(document)
        except PyMongoError as e:
            print("❌ Change stream error:", e)

    def start_watcher_thread(self):
        """
        Run the watcher in a separate thread.
        """
        watcher_thread = threading.Thread(target=self.watch_for_updates, daemon=True)
        watcher_thread.start()

    def get_next_insert(self, timeout=None):
        """
        Get next document inserted into MongoDB (if available), optionally with timeout.
        """
        try:
            return self.queue.get(timeout=timeout)
        except:
            return None
