import os
import pickle
from datetime import datetime
from support.settings import dest_dir


class FileManager:
    """Manages uploaded CV files and portfolio data"""
    
    def __init__(self):
        self.uploaded_files_dir = f"{dest_dir}/uploaded_files"
        # Use the same path as extractor's structured_cv_path
        self.portfolio_dir = dest_dir
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.uploaded_files_dir, exist_ok=True)
        # Portfolio directory is the same as dest_dir, so no need to create
    
    def save_uploaded_file(self, uploaded_file, original_filename):
        """Save uploaded file to the uploaded_files directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{original_filename}"
        file_path = os.path.join(self.uploaded_files_dir, safe_filename)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path, safe_filename
    
    def get_uploaded_files(self):
        """Get list of all uploaded files with metadata"""
        files = []
        if os.path.exists(self.uploaded_files_dir):
            for filename in os.listdir(self.uploaded_files_dir):
                file_path = os.path.join(self.uploaded_files_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    files.append({
                        'filename': filename,
                        'path': file_path,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'original_name': filename.split('_', 1)[1] 
                        if '_' in filename else filename
                    })
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
    
    def delete_uploaded_file(self, filename):
        """Delete a specific uploaded file"""
        file_path = os.path.join(self.uploaded_files_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def save_portfolio_data(self, structured_cv, filename="structured_cv.pkl"):
        """Save portfolio data to the same location as extractor's 
        structured_cv_path"""
        file_path = os.path.join(self.portfolio_dir, filename)
        with open(file_path, 'wb') as f:
            pickle.dump(structured_cv, f)
        return file_path
    
    def load_portfolio_data(self, filename="structured_cv.pkl"):
        """Load portfolio data from the same location as extractor's 
        structured_cv_path"""
        file_path = os.path.join(self.portfolio_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def has_portfolio_data(self, filename="structured_cv.pkl"):
        """Check if portfolio data exists in the same location as 
        extractor's structured_cv_path"""
        file_path = os.path.join(self.portfolio_dir, filename)
        return os.path.exists(file_path)
    
    def get_portfolio_files(self):
        """Get list of portfolio data files from the same location as 
        extractor"""
        files = []
        if os.path.exists(self.portfolio_dir):
            for filename in os.listdir(self.portfolio_dir):
                # Only include pickle files that could be portfolio data
                if filename.lower() == "structured_cv.pkl":
                # if (filename.endswith('.pkl') and 
                #         'cv' in filename.lower()):
                    file_path = os.path.join(self.portfolio_dir, filename)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        files.append({
                            'filename': filename,
                            'path': file_path,
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime)
                        })
        
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
