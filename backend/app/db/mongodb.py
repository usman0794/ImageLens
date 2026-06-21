from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings


class MongoDB:
    """
    MongoDB Atlas Connection Manager

    Responsibilities:
    - Create MongoDB connection
    - Return database instance
    - Close connection on shutdown
    """

    client: AsyncIOMotorClient = None
    database = None

    @classmethod
    async def connect(cls):
        """
        Connect to MongoDB Atlas
        """

        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)

        cls.database = cls.client[settings.MONGODB_DB_NAME]

        # Verify connection
        await cls.client.admin.command("ping")

        print("✅ MongoDB Atlas Connected")

    @classmethod
    async def close(cls):
        """
        Close MongoDB connection
        """

        if cls.client:
            cls.client.close()
            print("🔴 MongoDB Connection Closed")

    @classmethod
    def get_database(cls):
        """
        Return database instance
        """

        return cls.database