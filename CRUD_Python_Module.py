# Aniekan Udoessien - CS 340 - Client/Server Development

from typing import Any
from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, user_name: str, password: str, host: str, port: int, database: str, collection: str):
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = user_name 
        PASS = password 
        HOST = host
        PORT = port
        DB = database
        COL = collection
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Complete a create method to implement the C in CRUD.
    def create(self, documents: list[dict[str, Any]]) -> bool:
        # validate that documents is not None
        if not documents:
            # throw exception
            raise ValueError("Documents must be a non-empty list.")
            
        # validate that every item is a dictionary.
        if not all(isinstance(document, dict) for document in documents):
            raise ValueError("Every item in documents must be a dictionary.")

        # insulate create operation within a try block
        try:
            # insert the list of documents to the collection
            self.collection.insert_many(documents)
            return True

        # catch any exceptions
        except Exception as e:
            # log the failed insertion operation
            print(f"Insertion operation failed: {e}")
            return False

    # Complete a query method to implement the R in CRUD.
    def query(self, match: dict) -> list:

        # create empty list
        results = []

        try:
            # fetch the matching documents from the collection
            cursor = self.collection.find(match)

            # iterate over the cursor using a for loop
            for document in cursor:
                # append each document to the result list
                results.append(document)

            # return the results
            return results

        except Exception as e:
            # raise a RuntimeError when the query operation fails
            raise Exception(f"Query operation failed: {e}") from e


    # Complete an update method to implement the U in CRUD
    def update(self, match: dict, document: dict) -> int:
        # raise a ValueError exception if no match argument is passed
        if not match:
            raise ValueError("A match condition is required")

        # raise a ValueError exception if no document argument is passed
        if document is None:
            raise ValueError("Nothing to save, because data parameter is empty")

        # wrap the update operation in a try - except block to handle any exceptions
        try:
            # execute the update operation, passing the match
            # and document variables as arguments
            result = self.collection.update_many(match, document)
            # return the number of documents successfully modified
            return result.modified_count
        except Exception as e:
            # raise a RuntimeError when update operation fails
            raise RuntimeError(f"Update operation failed: {e}") from e


    # Complete a delete method to implement the D in CRUD
    def delete(self, match: dict) -> int:
        # raise a ValueError exception if no match parameter is passed
        if not match:
            raise ValueError("Nothing to save, because data parameter is empty")

        # wrap the delete operation in a try - except block to handle any exceptions
        try:
            # execute the delete operation, passing the match argument
            result = self.collection.delete_many(match)
            # return the number of documents successfully deleted
            return result.deleted_count
        except Exception as e:
            # raise a RuntimeError when the delete operation fails
            raise RuntimeError(f"Delete operation failed: {e}") from e