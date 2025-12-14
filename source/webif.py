#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
IPAudio Web Interface for Multi-Category Playlist Management
Access at: http://box-ip:8080/ipaudio
"""
from Components.config import config
from Plugins.Extensions.IPAudio.plugin import getPlaylistDir
from twisted.web import resource, server
import json
import os
import glob

def getPlaylistDirWeb():
    path = config.plugins.IPAudio.settingsPath.value
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            pass
    return path

class IPAudioAPI(resource.Resource):
    """API endpoints for playlist management"""
    isLeaf = True
    
    def render_GET(self, request):
        """Handle GET requests"""
        request.setHeader(b"content-type", b"application/json")
        request.setHeader(b"Access-Control-Allow-Origin", b"*")
        
        path = request.path.decode('utf-8')
        
        if path.endswith('/categories'):
            return self.getCategories()
        elif path.endswith('/playlist'):
            # Get category from query parameter
            category = request.args.get(b'category', [b''])[0].decode('utf-8')
            return self.getPlaylist(category)
        else:
            return b'{"error": "Unknown endpoint"}'
    
    def render_POST(self, request):
        """Handle POST requests"""
        request.setHeader(b"content-type", b"application/json")
        request.setHeader(b"Access-Control-Allow-Origin", b"*")
        
        path = request.path.decode('utf-8')
        
        if path.endswith('/save'):
            return self.savePlaylist(request)
        elif path.endswith('/create-category'):
            return self.createCategory(request)
        elif path.endswith('/delete-category'):
            return self.deleteCategory(request)
        elif path.endswith('/rename-category'):
            return self.renameCategory(request)
        else:
            return b'{"error": "Unknown endpoint"}'
    
    def getCategories(self):
        """Return list of all playlist categories"""
        try:
            playlist_dir = getPlaylistDirWeb()
            # Create directory if not exists
            if not os.path.exists(playlist_dir):
                os.makedirs(playlist_dir)
            
            categories = []
            files = glob.glob(playlist_dir + 'ipaudio_*.json')
            
            for filepath in sorted(files):
                filename = os.path.basename(filepath)
                category = filename.replace('ipaudio_', '').replace('.json', '')
                
                # Count channels
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        count = len(data.get('playlist', []))
                except:
                    count = 0
                
                categories.append({
                    'name': category,
                    'display_name': category.capitalize(),
                    'count': count,
                    'file': filename
                })
            
            return json.dumps({'categories': categories}).encode('utf-8')
        except Exception as e:
            return json.dumps({'error': str(e)}).encode('utf-8')
    
    def getPlaylist(self, category):
        """Return playlist for specific category"""
        playlist_dir = getPlaylistDirWeb()
        try:
            if not category:
                return b'{"error": "No category specified"}'
            
            filepath = playlist_dir + 'ipaudio_{}.json'.format(category)
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = f.read()
                return data.encode('utf-8')
            else:
                return b'{"playlist": []}'
        except Exception as e:
            return json.dumps({'error': str(e)}).encode('utf-8')
    
    def savePlaylist(self, request):
        """Save playlist for category"""
        playlist_dir = getPlaylistDirWeb()
        try:
            content = request.content.read()
            data = json.loads(content.decode('utf-8'))
            
            category = data.get('category')
            playlist = data.get('playlist')
            
            if not category:
                return b'{"success": false, "error": "No category specified"}'
            
            filepath = playlist_dir + 'ipaudio_{}.json'.format(category)
            
            with open(filepath, 'w') as f:
                json.dump({'playlist': playlist}, f, indent=4)
            
            return b'{"success": true}'
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}).encode('utf-8')
    
    def createCategory(self, request):
        """Create new category"""
        playlist_dir = getPlaylistDirWeb()
        try:
            content = request.content.read()
            data = json.loads(content.decode('utf-8'))
            
            category = data.get('category', '').lower().strip()
            
            if not category:
                return b'{"success": false, "error": "Category name required"}'
            
            # Validate category name (alphanumeric and underscore only)
            if not category.replace('_', '').isalnum():
                return b'{"success": false, "error": "Invalid category name"}'
            
            filepath = playlist_dir + 'ipaudio_{}.json'.format(category)
            
            if os.path.exists(filepath):
                return b'{"success": false, "error": "Category already exists"}'
            
            # Create empty playlist
            with open(filepath, 'w') as f:
                json.dump({'playlist': []}, f, indent=4)
            
            return b'{"success": true}'
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}).encode('utf-8')
    
    def deleteCategory(self, request):
        """Delete category"""
        playlist_dir = getPlaylistDirWeb()
        try:
            content = request.content.read()
            data = json.loads(content.decode('utf-8'))
            
            category = data.get('category', '').lower().strip()
            
            if not category:
                return b'{"success": false, "error": "Category name required"}'
            
            filepath = playlist_dir + 'ipaudio_{}.json'.format(category)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return b'{"success": true}'
            else:
                return b'{"success": false, "error": "Category not found"}'
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}).encode('utf-8')
    
    def renameCategory(self, request):
        """Rename category"""
        playlist_dir = getPlaylistDirWeb()
        try:
            content = request.content.read()
            data = json.loads(content.decode('utf-8'))
            
            old_name = data.get('old_name', '').lower().strip()
            new_name = data.get('new_name', '').lower().strip()
            
            if not old_name or not new_name:
                return b'{"success": false, "error": "Both names required"}'
            
            # Validate new name
            if not new_name.replace('_', '').isalnum():
                return b'{"success": false, "error": "Invalid category name"}'
            
            old_file = playlist_dir + 'ipaudio_{}.json'.format(old_name)
            new_file = playlist_dir + 'ipaudio_{}.json'.format(new_name)
            
            if not os.path.exists(old_file):
                return b'{"success": false, "error": "Category not found"}'
            
            if os.path.exists(new_file):
                return b'{"success": false, "error": "New category name already exists"}'
            
            os.rename(old_file, new_file)
            return b'{"success": true}'
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}).encode('utf-8')

class IPAudioWebInterface(resource.Resource):
    """Main web interface"""
    
    def __init__(self):
        resource.Resource.__init__(self)
        # Register API endpoints
        api = resource.Resource()
        api.putChild(b"categories", IPAudioAPI())
        api.putChild(b"playlist", IPAudioAPI())
        api.putChild(b"save", IPAudioAPI())
        api.putChild(b"create-category", IPAudioAPI())
        api.putChild(b"delete-category", IPAudioAPI())
        api.putChild(b"rename-category", IPAudioAPI())
        self.putChild(b"api", api)
    
    def getChild(self, path, request):
        if path == b"":
            return self
        return resource.Resource.getChild(self, path, request)
    
    def render_GET(self, request):
        """Serve the HTML interface"""
        request.setHeader(b"content-type", b"text/html; charset=utf-8")
        return self.getHTML().encode('utf-8')
    
    def getHTML(self):
        """Generate modern HTML interface with drag-drop"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPAudio Manager</title>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .main {
            display: flex;
            min-height: 600px;
        }
        .sidebar {
            width: 300px;
            background: #f8f9fa;
            border-right: 1px solid #dee2e6;
            padding: 20px;
        }
        .content {
            flex: 1;
            padding: 30px;
        }
        
        .category-item {
            padding: 15px;
            margin-bottom: 10px;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .category-item:hover {
            transform: translateX(5px);
            border-color: #667eea;
        }
        .category-item.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .category-badge {
            background: rgba(0,0,0,0.1);
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        
        button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            margin-right: 10px;
        }
        button:hover { background: #5568d3; transform: translateY(-2px); }
        button.success { background: #27ae60; }
        button.success:hover { background: #229954; }
        button.danger { background: #e74c3c; }
        button.danger:hover { background: #c0392b; }
        button.small { padding: 6px 12px; font-size: 12px; }
        
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .channel-list {
            border: 1px solid #dee2e6;
            border-radius: 8px;
            max-height: 500px;
            overflow-y: auto;
        }
        .channel-item-list {
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: move;
            transition: background 0.2s;
        }
        .channel-item-list:hover { background: #f8f9fa; }
        .channel-item-list.sortable-ghost {
            opacity: 0.4;
            background: #667eea;
        }
        .channel-item-list.sortable-drag {
            background: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .channel-info {
            flex: 1;
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .drag-handle {
            cursor: move;
            color: #999;
            font-size: 20px;
        }
        .channel-number {
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            min-width: 40px;
            text-align: center;
        }
        .channel-name {
            font-weight: 600;
            color: #333;
            flex: 1;
        }
        .channel-url {
            color: #666;
            font-size: 12px;
            flex: 2;
            word-break: break-all;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal.active { display: flex; }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .modal-content h2 {
            margin-bottom: 20px;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #666;
            font-weight: 600;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .empty-state {
            padding: 60px 20px;
            text-align: center;
            color: #999;
        }
        .empty-state-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .stats {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            flex: 1;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 IPAudio Playlist Manager</h1>
            <p>Manage your audio channels by category</p>
        </div>
        
        <div class="main">
            <div class="sidebar">
                <button class="success" style="width: 100%; margin-bottom: 15px;" onclick="showCreateCategoryModal()">
                    ➕ New Category
                </button>
                <div id="categoryList"></div>
            </div>
            
            <div class="content">
                <div id="categoryContent">
                    <div class="empty-state">
                        <div class="empty-state-icon">📁</div>
                        <h3>Select a category</h3>
                        <p>Choose a category from the sidebar or create a new one</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Channel Modal -->
    <div class="modal" id="channelModal">
        <div class="modal-content">
            <h2 id="channelModalTitle">Add Channel</h2>
            <div class="form-group">
                <label>Channel Name</label>
                <input type="text" id="channelName" placeholder="Enter channel name">
            </div>
            <div class="form-group">
                <label>Stream URL</label>
                <input type="text" id="channelUrl" placeholder="http://...">
            </div>
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                <button onclick="closeModal('channelModal')">Cancel</button>
                <button class="success" onclick="saveChannel()">Save</button>
            </div>
        </div>
    </div>
    
    <!-- Category Modal -->
    <div class="modal" id="categoryModal">
        <div class="modal-content">
            <h2 id="categoryModalTitle">Create Category</h2>
            <div class="form-group">
                <label>Category Name</label>
                <input type="text" id="categoryName" placeholder="e.g., sport, quran, music">
            </div>
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                <button onclick="closeModal('categoryModal')">Cancel</button>
                <button class="success" onclick="saveCategory()">Create</button>
            </div>
        </div>
    </div>
    
    <script>
        let categories = [];
        let currentCategory = null;
        let playlist = [];
        let editIndex = -1;
        let sortable = null;
        
        const API = {
            getCategories: () => fetch('/ipaudio/api/categories').then(r => r.json()),
            getPlaylist: (cat) => fetch('/ipaudio/api/playlist?category=' + cat).then(r => r.json()),
            savePlaylist: (cat, data) => fetch('/ipaudio/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: cat, playlist: data })
            }).then(r => r.json()),
            createCategory: (name) => fetch('/ipaudio/api/create-category', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: name })
            }).then(r => r.json()),
            deleteCategory: (name) => fetch('/ipaudio/api/delete-category', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: name })
            }).then(r => r.json()),
            renameCategory: (oldName, newName) => fetch('/ipaudio/api/rename-category', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ old_name: oldName, new_name: newName })
            }).then(r => r.json())
        };
        
        window.onload = () => loadCategories();
        
        function loadCategories() {
            API.getCategories().then(data => {
                categories = data.categories || [];
                renderCategories();
            }).catch(err => alert('Error loading categories: ' + err));
        }
        
        function renderCategories() {
            const container = document.getElementById('categoryList');
            container.innerHTML = categories.map(cat => `
                <div class="category-item ${currentCategory === cat.name ? 'active' : ''}" 
                     onclick="selectCategory('${cat.name}')">
                    <div>
                        <strong>${cat.display_name}</strong>
                    </div>
                    <span class="category-badge">${cat.count}</span>
                </div>
            `).join('');
        }
        
        function selectCategory(catName) {
            currentCategory = catName;
            renderCategories();
            loadPlaylist(catName);
        }
        
        function loadPlaylist(catName) {
            API.getPlaylist(catName).then(data => {
                playlist = data.playlist || [];
                renderPlaylist();
            }).catch(err => alert('Error loading playlist: ' + err));
        }
        
        function renderPlaylist() {
            const container = document.getElementById('categoryContent');
            
            const categoryInfo = categories.find(c => c.name === currentCategory);
            const displayName = categoryInfo ? categoryInfo.display_name : currentCategory;
            
            let html = `
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">${playlist.length}</div>
                        <div class="stat-label">Channels</div>
                    </div>
                </div>
                
                <div class="controls">
                    <button class="success" onclick="showAddChannelModal()">➕ Add Channel</button>
                    <button onclick="loadPlaylist('${currentCategory}')">🔄 Refresh</button>
                    <button class="danger" onclick="deleteCurrentCategory()">🗑️ Delete Category</button>
                </div>
                
                <div class="channel-list" id="channelList">
            `;
            
            if (playlist.length === 0) {
                html += '<div class="empty-state"><div class="empty-state-icon">🎵</div><p>No channels yet. Add one!</p></div>';
            } else {
                html += playlist.map((ch, idx) => `
                    <div class="channel-item-list" data-index="${idx}">
                        <div class="channel-info">
                            <span class="drag-handle">☰</span>
                            <div class="channel-number">${idx + 1}</div>
                            <div class="channel-name">${escapeHtml(ch.channel)}</div>
                            <div class="channel-url">${escapeHtml(ch.url)}</div>
                        </div>
                        <div>
                            <button class="small" onclick="editChannel(${idx})">✏️</button>
                            <button class="small danger" onclick="deleteChannel(${idx})">🗑️</button>
                        </div>
                    </div>
                `).join('');
            }
            
            html += '</div>';
            container.innerHTML = html;
            
            // Initialize Sortable.js for drag-drop
            if (playlist.length > 0) {
                const listEl = document.getElementById('channelList');
                if (sortable) sortable.destroy();
                sortable = Sortable.create(listEl, {
                    animation: 150,
                    ghostClass: 'sortable-ghost',
                    dragClass: 'sortable-drag',
                    handle: '.drag-handle',
                    onEnd: function(evt) {
                        // Reorder playlist array
                        const item = playlist.splice(evt.oldIndex, 1)[0];
                        playlist.splice(evt.newIndex, 0, item);
                        savePlaylistData();
                    }
                });
            }
        }
        
        function showAddChannelModal() {
            editIndex = -1;
            document.getElementById('channelModalTitle').textContent = 'Add Channel';
            document.getElementById('channelName').value = '';
            document.getElementById('channelUrl').value = '';
            document.getElementById('channelModal').classList.add('active');
        }
        
        function editChannel(idx) {
            editIndex = idx;
            const ch = playlist[idx];
            document.getElementById('channelModalTitle').textContent = 'Edit Channel';
            document.getElementById('channelName').value = ch.channel;
            document.getElementById('channelUrl').value = ch.url;
            document.getElementById('channelModal').classList.add('active');
        }
        
        function saveChannel() {
            const name = document.getElementById('channelName').value.trim();
            const url = document.getElementById('channelUrl').value.trim();
            
            if (!name || !url) {
                alert('Please fill in both fields');
                return;
            }
            
            const channel = { channel: name, url: url };
            
            if (editIndex >= 0) {
                playlist[editIndex] = channel;
            } else {
                playlist.push(channel);
            }
            
            savePlaylistData();
        }
        
        function deleteChannel(idx) {
            if (!confirm('Delete this channel?')) return;
            playlist.splice(idx, 1);
            savePlaylistData();
        }
        
        function savePlaylistData() {
            API.savePlaylist(currentCategory, playlist).then(data => {
                if (data.success) {
                    closeModal('channelModal');
                    loadCategories();
                    renderPlaylist();
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            }).catch(err => alert('Error: ' + err));
        }
        
        function showCreateCategoryModal() {
            document.getElementById('categoryName').value = '';
            document.getElementById('categoryModal').classList.add('active');
        }
        
        function saveCategory() {
            const name = document.getElementById('categoryName').value.trim().toLowerCase();
            
            if (!name) {
                alert('Please enter a category name');
                return;
            }
            
            if (!/^[a-z0-9_]+$/.test(name)) {
                alert('Only lowercase letters, numbers and underscores allowed');
                return;
            }
            
            API.createCategory(name).then(data => {
                if (data.success) {
                    closeModal('categoryModal');
                    loadCategories();
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            }).catch(err => alert('Error: ' + err));
        }
        
        function deleteCurrentCategory() {
            if (!confirm(`Delete category "${currentCategory}" and all its channels?`)) return;
            
            API.deleteCategory(currentCategory).then(data => {
                if (data.success) {
                    currentCategory = null;
                    loadCategories();
                    document.getElementById('categoryContent').innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">📁</div>
                            <h3>Select a category</h3>
                        </div>
                    `;
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            }).catch(err => alert('Error: ' + err));
        }
        
        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""

# Global reference
_webif_root = None

def startWebInterface():
    """Start web interface"""
    global _webif_root
    try:
        from twisted.internet import reactor
        
        root = resource.Resource()
        root.putChild(b"ipaudio", IPAudioWebInterface())
        _webif_root = root
        
        site = server.Site(root)
        reactor.listenTCP(8080, site, interface='0.0.0.0')
        
        print("[IPAudio WebIF] Started on http://0.0.0.0:8080/ipaudio")
        return True
    except Exception as e:
        print("[IPAudio WebIF] Error: {}".format(e))
        import traceback
        traceback.print_exc()
        return False
