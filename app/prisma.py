from prisma import Prisma

# Create a singleton Prisma client
prisma = Prisma()


async def connect_prisma():
    """Connect to the Prisma database if not already connected."""
    if not prisma.is_connected():
        await prisma.connect()


async def disconnect_prisma():
    """Disconnect from the Prisma database."""
    if prisma.is_connected():
        await prisma.disconnect()
