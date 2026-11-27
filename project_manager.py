"""
Project Manager - Orchestrates all modules and manages data flow between components
"""
import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from database import DatabaseManager
from figma_handler import FigmaHandler
from streamlit_builder import StreamlitUIBuilder


class ProjectManager:
    """Central manager that coordinates all project-related operations"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.figma_handler = FigmaHandler()
        self.streamlit_builder = StreamlitUIBuilder()
        self.current_project: Dict[str, Any] = {}
        self.projects_directory = Path(os.getcwd()) / "projects"
        self.models_directory = Path(os.getcwd()) / "models"
        
        # Create necessary directories
        self.projects_directory.mkdir(exist_ok=True)
        self.models_directory.mkdir(exist_ok=True)

    def create_new_project(self, project_data: Dict[str, Any]) -> int:
        """
        Create a new project with all necessary data
        
        Args:
            project_data: Dict containing name, description, project_type, programming_language
            
        Returns:
            Project ID from database
        """
        # Save to database
        project_id = self.db_manager.save_project(project_data)
        
        # Create project directory
        project_dir = self.projects_directory / f"project_{project_id}"
        project_dir.mkdir(exist_ok=True)
        
        # Store current project
        self.current_project = {
            'id': project_id,
            'directory': str(project_dir),
            **project_data
        }
        
        return project_id

    def save_figma_design(self, figma_url: str, figma_token: str, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Download and process Figma design
        
        Args:
            figma_url: URL of the Figma project
            figma_token: Figma API token
            project_id: Project ID from database
            
        Returns:
            Design data dictionary or None if failed
        """
        try:
            project_name = f"project_{project_id}"
            design_data = self.figma_handler.fetch_design(figma_url, figma_token, project_name)
            
            if design_data:
                # Save design to project directory
                project_dir = self.projects_directory / f"project_{project_id}"
                design_file = project_dir / "figma_design.json"
                
                with open(design_file, 'w') as f:
                    json.dump(design_data, f, indent=2)
                
                # Update database
                self.db_manager.update_project_design(project_id, str(design_file))
                
                return design_data
        except Exception as e:
            print(f"Error saving Figma design: {str(e)}")
            return None

    def build_streamlit_app(self, components: List[Dict[str, Any]], project_id: int) -> Optional[str]:
        """
        Build Streamlit app from dragged components
        
        Args:
            components: List of components from drag & drop
            project_id: Project ID from database
            
        Returns:
            Path to generated Streamlit app or None if failed
        """
        try:
            # Generate Streamlit code
            project_name = f"project_{project_id}"
            code = self.streamlit_builder.generate_app_code(components, project_name)
            
            if code:
                # Save to project directory
                project_dir = self.projects_directory / f"project_{project_id}"
                app_file = project_dir / "streamlit_app.py"
                
                with open(app_file, 'w') as f:
                    f.write(code)
                
                # Update database
                self.db_manager.update_project_streamlit(project_id, str(app_file))
                
                return str(app_file)
        except Exception as e:
            print(f"Error building Streamlit app: {str(e)}")
            return None

    def save_user_credentials(self, credentials: Dict[str, str], project_id: int) -> bool:
        """
        Save user credentials (API keys, tokens, etc.)
        
        Args:
            credentials: Dict of API keys and credentials
            project_id: Project ID from database
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project_dir = self.projects_directory / f"project_{project_id}"
            config_file = project_dir / "credentials.json"
            
            # Encrypt and save credentials
            with open(config_file, 'w') as f:
                json.dump(credentials, f, indent=2)
            
            # Update database
            self.db_manager.update_project_credentials(project_id, str(config_file))
            
            return True
        except Exception as e:
            print(f"Error saving credentials: {str(e)}")
            return False

    def get_project_structure(self, project_id: int) -> Dict[str, Any]:
        """Get complete project structure and status"""
        project_dir = self.projects_directory / f"project_{project_id}"
        
        return {
            'id': project_id,
            'directory': str(project_dir),
            'design_exists': (project_dir / "figma_design.json").exists(),
            'app_exists': (project_dir / "streamlit_app.py").exists(),
            'credentials_exists': (project_dir / "credentials.json").exists(),
            'config_exists': (project_dir / "config.json").exists()
        }

    def export_project(self, project_id: int) -> Optional[str]:
        """
        Export complete project as a package
        
        Args:
            project_id: Project ID to export
            
        Returns:
            Path to exported project file or None
        """
        try:
            project_dir = self.projects_directory / f"project_{project_id}"
            export_name = f"project_{project_id}_export.zip"
            
            # Create zip file of project
            import shutil
            export_path = self.projects_directory / export_name
            shutil.make_archive(str(export_path.with_suffix('')), 'zip', project_dir)
            
            return str(export_path)
        except Exception as e:
            print(f"Error exporting project: {str(e)}")
            return None

    def delete_project(self, project_id: int) -> bool:
        """
        Delete project and all associated files
        
        Args:
            project_id: Project ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project_dir = self.projects_directory / f"project_{project_id}"
            
            # Remove directory
            import shutil
            if project_dir.exists():
                shutil.rmtree(project_dir)
            
            # Delete from database
            # Note: Add delete method to DatabaseManager if needed
            
            return True
        except Exception as e:
            print(f"Error deleting project: {str(e)}")
            return False

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Get all projects from database"""
        return self.db_manager.get_projects()

    def generate_deployment_guide(self, project_id: int) -> str:
        """Generate deployment instructions for the project"""
        project_structure = self.get_project_structure(project_id)
        
        guide = f"""
# Panduan Deployment Project {project_id}

## Struktur Project
- Design: {'✓ Ada' if project_structure['design_exists'] else '✗ Tidak ada'}
- Streamlit App: {'✓ Ada' if project_structure['app_exists'] else '✗ Tidak ada'}
- Credentials: {'✓ Ada' if project_structure['credentials_exists'] else '✗ Tidak ada'}

## Langkah-langkah Deployment

### 1. Install Dependencies
```bash
pip install streamlit requests
```

### 2. Setup Environment Variables
Buat file `.env` dengan kredensial dari `credentials.json`

### 3. Run Streamlit App
```bash
streamlit run streamlit_app.py
```

### 4. Access Application
Buka browser ke `http://localhost:8501`

## Tips & Troubleshooting
- Pastikan semua dependencies terinstall
- Periksa API keys di credentials.json
- Lihat Figma design untuk referensi UI/UX
"""
        return guide
