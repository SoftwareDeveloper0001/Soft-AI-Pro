import os
import json
from datetime import datetime
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class FigmaHandler:
    def __init__(self):
        self.upload_dir = os.path.join(os.getcwd(), "designs")
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_figma_design(self, file_path: str, project_name: str) -> Dict[str, Any]:
        """Save uploaded Figma design file"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

            # Create project-specific directory
            project_dir = os.path.join(self.upload_dir, project_name.replace(' ', '_'))
            os.makedirs(project_dir, exist_ok=True)

            # Copy file to project directory
            filename = os.path.basename(file_path)
            destination = os.path.join(project_dir, filename)
            
            with open(file_path, 'rb') as src:
                with open(destination, 'wb') as dst:
                    dst.write(src.read())

            design_data: Dict[str, Any] = {
                'filename': filename,
                'path': destination,
                'project_name': project_name,
                'uploaded_at': datetime.now().isoformat(),
                'file_size': os.path.getsize(destination)
            }

            # Save metadata
            metadata_path = os.path.join(project_dir, 'metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(design_data, f, indent=2)

            return {
                'success': True,
                'message': f'Design berhasil disimpan: {filename}',
                'data': design_data
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error menyimpan design: {str(e)}',
                'error': str(e)
            }

    def fetch_figma_via_api(self, figma_url: str, api_key: str, project_name: str) -> Dict[str, Any]:
        """Fetch Figma design via Figma API"""
        try:
            # Extract file ID dari URL
            # Format: https://www.figma.com/file/{FILE_ID}/...
            if '/file/' not in figma_url:
                raise ValueError("URL Figma tidak valid")

            file_id = figma_url.split('/file/')[1].split('/')[0]
            
            # API endpoint
            api_url = f'https://api.figma.com/v1/files/{file_id}'
            
            # Create request dengan header
            request = urllib.request.Request(
                api_url,
                headers={'X-Figma-Token': api_key}
            )
            
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
            
            project_dir = os.path.join(self.upload_dir, project_name.replace(' ', '_'))
            os.makedirs(project_dir, exist_ok=True)

            figma_data: Dict[str, Any] = {
                'figma_file_id': file_id,
                'figma_url': figma_url,
                'project_name': project_name,
                'fetched_at': datetime.now().isoformat(),
                'figma_project_name': data.get('name', 'Unknown'),
                'last_modified': data.get('lastModified', '')
            }

            metadata_path = os.path.join(project_dir, 'figma_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(figma_data, f, indent=2)

            return {
                'success': True,
                'message': 'Figma design berhasil diambil dari API',
                'data': figma_data
            }
            
        except urllib.error.HTTPError as e:
            return {
                'success': False,
                'message': f'Error dari Figma API: {e.code}',
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error mengambil data dari Figma: {str(e)}',
                'error': str(e)
            }

    def fetch_design(self, figma_url: str, api_key: str, project_name: str = "default") -> Optional[Dict[str, Any]]:
        """Fetch Figma design and return normalized data"""
        result = self.fetch_figma_via_api(figma_url, api_key, project_name)
        if result.get('success'):
            return result.get('data')
        return None

    def get_design_info(self, project_name: str) -> Dict[str, Any]:
        """Get information about project design"""
        project_dir = os.path.join(self.upload_dir, project_name.replace(' ', '_'))
        
        if not os.path.exists(project_dir):
            return {'success': False, 'message': 'Design tidak ditemukan'}

        info: Dict[str, Any] = {
            'files': os.listdir(project_dir),
            'path': project_dir
        }

        # Check for metadata
        metadata_path = os.path.join(project_dir, 'metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                info['metadata'] = json.load(f)

        return {'success': True, 'data': info}