#!/usr/bin/env python3
"""
HealthGuard Backup Tool
Creates a compressed backup of the entire project
"""

import shutil
import os
from datetime import datetime

def create_backup():
    """Create a backup of the entire project"""
    
    # Define paths
    source_dir = r"C:\Mini Project"
    backup_dir = r"C:\Mini Project Backups"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"HealthGuard_Backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    print("\n" + "=" * 80)
    print("  HealthGuard Backup Tool")
    print("=" * 80 + "\n")
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Created backup directory: {backup_dir}\n")
    
    try:
        print(f"📦 Creating backup...")
        print(f"   Source: {source_dir}")
        print(f"   Backup: {backup_path}\n")
        
        # Create backup (excluding unnecessary files)
        shutil.copytree(
            source_dir,
            backup_path,
            ignore=shutil.ignore_patterns(
                '__pycache__',
                '*.pyc',
                '.git',
                'ngrok.zip',
                '*.log'
            )
        )
        
        # Calculate size
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(backup_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        
        size_mb = total_size / (1024 * 1024)
        
        print("✅ Backup created successfully!\n")
        print(f"Backup Location:")
        print(f"  📁 {backup_path}\n")
        print(f"Size: {size_mb:.2f} MB\n")
        
        # List backup contents
        print("📋 Backup Contents:")
        print("-" * 80)
        for root, dirs, files in os.walk(backup_path):
            level = root.replace(backup_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}📁 {os.path.basename(root)}/')
            sub_indent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f'{sub_indent}📄 {file}')
            if len(files) > 5:
                print(f'{sub_indent}... and {len(files) - 5} more files')
        
        print("\n" + "=" * 80)
        print("✨ Backup completed successfully!")
        print("=" * 80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating backup: {e}")
        return False

def create_zip_backup():
    """Create a ZIP file backup"""
    
    source_dir = r"C:\Mini Project"
    backup_dir = r"C:\Mini Project Backups"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"HealthGuard_Backup_{timestamp}.zip"
    zip_path = os.path.join(backup_dir, zip_name)
    
    print("\n" + "=" * 80)
    print("  Creating ZIP Backup")
    print("=" * 80 + "\n")
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Created backup directory: {backup_dir}\n")
    
    try:
        print(f"📦 Compressing project to ZIP...\n")
        
        shutil.make_archive(
            zip_path.replace('.zip', ''),
            'zip',
            source_dir
        )
        
        # Get file size
        zip_size = os.path.getsize(zip_path) / (1024 * 1024)
        
        print(f"✅ ZIP backup created successfully!\n")
        print(f"📦 Backup File: {zip_path}")
        print(f"📊 Size: {zip_size:.2f} MB\n")
        print("=" * 80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating ZIP backup: {e}")
        return False

def list_existing_backups():
    """List all existing backups"""
    
    backup_dir = r"C:\Mini Project Backups"
    
    if not os.path.exists(backup_dir):
        print("\n❌ No backup directory found!")
        return
    
    backups = os.listdir(backup_dir)
    
    if not backups:
        print("\n❌ No backups found!")
        return
    
    print("\n" + "=" * 80)
    print("  Existing Backups")
    print("=" * 80 + "\n")
    
    for i, backup in enumerate(sorted(backups), 1):
        backup_path = os.path.join(backup_dir, backup)
        if os.path.isdir(backup_path):
            size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                      for dirpath, dirnames, filenames in os.walk(backup_path) 
                      for filename in filenames) / (1024 * 1024)
            print(f"{i}. 📁 {backup}")
            print(f"   Size: {size:.2f} MB")
            print(f"   Type: Directory\n")
        else:
            size = os.path.getsize(backup_path) / (1024 * 1024)
            print(f"{i}. 📦 {backup}")
            print(f"   Size: {size:.2f} MB")
            print(f"   Type: ZIP File\n")
    
    print("=" * 80 + "\n")

def main_menu():
    """Display backup menu"""
    
    while True:
        print("\n" + "=" * 80)
        print("  HealthGuard Backup Tool - Protect Your Project")
        print("=" * 80)
        print("\nSelect backup option:")
        print("  1️⃣  Create Full Directory Backup")
        print("  2️⃣  Create ZIP File Backup (Compressed)")
        print("  3️⃣  List Existing Backups")
        print("  0️⃣  Exit")
        print("\n" + "-" * 80)
        
        choice = input("\nEnter your choice (0-3): ").strip()
        
        if choice == '1':
            create_backup()
        elif choice == '2':
            create_zip_backup()
        elif choice == '3':
            list_existing_backups()
        elif choice == '0':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    try:
        main_menu()
    except Exception as e:
        print(f"\n❌ Error: {e}")
