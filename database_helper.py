"""
Database Query Helper
Script untuk query dan manage SQLite database dengan mudah
"""

import sqlite3
import json
from datetime import datetime
from tabulate import tabulate

class DatabaseHelper:
    """Helper class untuk manage SQLite database"""
    
    def __init__(self, db_path: str = "soft_ai_pro.db"):
        self.db_path = db_path
    
    def query(self, sql: str, params: tuple = None, fetch_one: bool = False):
        """Execute query to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            if fetch_one:
                result = cursor.fetchone()
                result = dict(result) if result else None
            else:
                result = [dict(row) for row in cursor.fetchall()]
            
            conn.commit()
            conn.close()
            
            return result
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def show_all_projects(self):
        """Display all projects"""
        print("\n📋 All Projects:")
        print("=" * 80)
        
        projects = self.query("SELECT * FROM projects ORDER BY created_at DESC")
        
        if projects:
            headers = ['ID', 'Name', 'Type', 'Language', 'Status', 'Created']
            rows = []
            
            for p in projects:
                rows.append([
                    p['id'],
                    p['name'][:30],
                    p['project_type'],
                    p['programming_language'],
                    p['status'],
                    datetime.fromisoformat(p['created_at']).strftime('%Y-%m-%d %H:%M')
                ])
            
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print("❌ Tidak ada projects")
        
        print("=" * 80)
    
    def show_project_details(self, project_id: int):
        """Display project details"""
        print(f"\n📌 Project Details (ID: {project_id})")
        print("=" * 80)
        
        # Get project
        project = self.query(
            "SELECT * FROM projects WHERE id = ?",
            (project_id,),
            fetch_one=True
        )
        
        if not project:
            print("❌ Project tidak ditemukan")
            return
        
        print(f"\nProject Information:")
        print(f"  Name: {project['name']}")
        print(f"  Description: {project['description']}")
        print(f"  Type: {project['project_type']}")
        print(f"  Language: {project['programming_language']}")
        print(f"  Status: {project['status']}")
        print(f"  Created: {project['created_at']}")
        
        # Get features
        features = self.query(
            "SELECT * FROM features WHERE project_id = ? ORDER BY priority DESC",
            (project_id,)
        )
        
        if features:
            print(f"\n✨ Features ({len(features)}):")
            headers = ['ID', 'Name', 'Priority', 'Created']
            rows = []
            
            for f in features:
                rows.append([
                    f['id'],
                    f['name'],
                    f['priority'],
                    datetime.fromisoformat(f['created_at']).strftime('%Y-%m-%d')
                ])
            
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        
        # Get design pages
        pages = self.query(
            "SELECT * FROM design_pages WHERE project_id = ? ORDER BY page_number",
            (project_id,)
        )
        
        if pages:
            print(f"\n🎨 Design Pages ({len(pages)}):")
            headers = ['ID', 'Page', 'URL', 'Number']
            rows = []
            
            for p in pages:
                rows.append([
                    p['id'],
                    p['page_name'],
                    p['page_url'][:40] if p['page_url'] else 'N/A',
                    p['page_number']
                ])
            
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        
        print("=" * 80)
    
    def add_project(self, name: str, description: str, project_type: str, language: str):
        """Add new project"""
        try:
            sql = '''
                INSERT INTO projects (name, description, project_type, programming_language, status)
                VALUES (?, ?, ?, ?, 'created')
            '''
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql, (name, description, project_type, language))
            
            project_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Project berhasil ditambahkan (ID: {project_id})")
            return project_id
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def add_feature(self, project_id: int, name: str, priority: str = 'medium'):
        """Add feature to project"""
        try:
            sql = '''
                INSERT INTO features (project_id, name, priority)
                VALUES (?, ?, ?)
            '''
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql, (project_id, name, priority))
            
            feature_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Feature berhasil ditambahkan (ID: {feature_id})")
            return feature_id
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def delete_project(self, project_id: int):
        """Delete project and all related data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete will cascade due to foreign keys
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Project {project_id} dan semua datanya berhasil dihapus")
            return True
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def export_to_json(self, project_id: int, filename: str = None):
        """Export project to JSON"""
        if not filename:
            filename = f"project_{project_id}.json"
        
        try:
            project = self.query(
                "SELECT * FROM projects WHERE id = ?",
                (project_id,),
                fetch_one=True
            )
            
            if not project:
                print("❌ Project tidak ditemukan")
                return
            
            features = self.query(
                "SELECT * FROM features WHERE project_id = ?",
                (project_id,)
            )
            
            pages = self.query(
                "SELECT * FROM design_pages WHERE project_id = ?",
                (project_id,)
            )
            
            export_data = {
                'project': project,
                'features': features,
                'design_pages': pages
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"✅ Project berhasil export ke: {filename}")
            return filename
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None


def main():
    """Main menu"""
    db = DatabaseHelper()
    
    while True:
        print("\n" + "="*50)
        print("🗄️  Database Query Helper")
        print("="*50)
        print("1. Lihat semua projects")
        print("2. Lihat detail project")
        print("3. Tambah project baru")
        print("4. Tambah feature")
        print("5. Hapus project")
        print("6. Export ke JSON")
        print("7. Keluar")
        print("="*50)
        
        choice = input("Pilih menu (1-7): ").strip()
        
        if choice == '1':
            db.show_all_projects()
        
        elif choice == '2':
            try:
                project_id = int(input("Masukkan project ID: "))
                db.show_project_details(project_id)
            except ValueError:
                print("❌ Input tidak valid")
        
        elif choice == '3':
            name = input("Nama project: ")
            desc = input("Deskripsi: ")
            ptype = input("Tipe project: ")
            lang = input("Bahasa pemrograman: ")
            db.add_project(name, desc, ptype, lang)
        
        elif choice == '4':
            try:
                project_id = int(input("Project ID: "))
                fname = input("Nama feature: ")
                priority = input("Priority (low/medium/high): ")
                db.add_feature(project_id, fname, priority)
            except ValueError:
                print("❌ Input tidak valid")
        
        elif choice == '5':
            try:
                project_id = int(input("Project ID yang ingin dihapus: "))
                confirm = input("Yakin? (yes/no): ")
                if confirm.lower() == 'yes':
                    db.delete_project(project_id)
            except ValueError:
                print("❌ Input tidak valid")
        
        elif choice == '6':
            try:
                project_id = int(input("Project ID: "))
                db.export_to_json(project_id)
            except ValueError:
                print("❌ Input tidak valid")
        
        elif choice == '7':
            print("👋 Terima kasih!")
            break
        
        else:
            print("❌ Menu tidak valid")


if __name__ == "__main__":
    main()
