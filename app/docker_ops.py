import docker
import logging
from docker.errors import APIError, ImageNotFound

logger = logging.getLogger(__name__)

def get_docker_client():
    """Returns a configured Docker client."""
    try:
        client = docker.from_env()
        # Test connection
        client.ping()
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Docker daemon: {e}")
        raise RuntimeError("Could not connect to Docker daemon. Is Docker running?") from e

def pull_image(image_name: str) -> None:
    """
    Pulls the specified Docker image.
    
    Args:
        image_name (str): The name of the image to pull (e.g., 'python:3.9-alpine').
    """
    client = get_docker_client()
    logger.info(f"Pulling image: {image_name}...")
    try:
        client.images.pull(image_name)
        logger.info(f"Successfully pulled image: {image_name}")
    except APIError as e:
        logger.error(f"Failed to pull image {image_name}: {e}")
        raise RuntimeError(f"Failed to pull image {image_name}") from e

def cleanup_image(image_name: str) -> None:
    """
    Removes the specified Docker image locally to save space.
    
    Args:
        image_name (str): The name of the image to remove.
    """
    client = get_docker_client()
    logger.info(f"Cleaning up image: {image_name}...")
    try:
        client.images.remove(image_name, force=True)
        logger.info(f"Successfully removed image: {image_name}")
    except ImageNotFound:
        logger.warning(f"Image {image_name} not found during cleanup.")
    except APIError as e:
        logger.error(f"Failed to remove image {image_name}: {e}")
        # Not raising here as cleanup failure shouldn't fail the pipeline
