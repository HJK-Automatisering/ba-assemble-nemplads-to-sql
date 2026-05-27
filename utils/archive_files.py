import logging
import os
import shutil

logger = logging.getLogger(__name__)

def archive_files(file_path: str) -> None:
    '''
    Description:
        Clears the archive folder and moves all files from the source
        folder into it.

    Flow:
        1. Delete all files in the archive subfolder.
        2. Move all files from file_path into the archive subfolder.

    Args:
        file_path (str): Path to the source folder containing files to archive.
            Must contain an 'Arkiv' subfolder.

    Returns:
        None.

    Raises:
        FileNotFoundError: If file_path or the Arkiv subfolder does not exist.
        PermissionError: If the process lacks permission to delete or move files.
    '''
    
    archive_path = os.path.join(file_path, 'Arkiv')

    # Delete all files in archive
    for f in os.listdir(archive_path):
        full_path = os.path.join(archive_path, f)
        if os.path.isfile(full_path):
            os.remove(full_path)
            logger.info('Deleted from archive: %s', f)
    logger.info('Archive cleared')

    # Move all files from FILE_PATH to archive
    for f in os.listdir(file_path):
        full_path = os.path.join(file_path, f)
        if os.path.isfile(full_path):
            shutil.move(full_path, os.path.join(archive_path, f))
            logger.info('Moved to archive: %s', f)
    logger.info('Files archived')