from vedo import *
import json
import numpy as np
import time

class SkeletonAnimatorVedo:
    def __init__(self, json_file):
        """Initialise l'animateur de squelette avec Vedo"""
        # Charger les données d'animation
        with open(json_file, 'r') as f:
            self.animation_data = json.load(f)
        
        print(f"Animation chargée: {len(self.animation_data)} frames")
        
        # Définir les connexions entre les os
        self.bone_connections = [
            # Torse
            ("shoulder.L", "shoulder.R"),
            ("shoulder.L", "thigh.L"),
            ("shoulder.R", "thigh.R"),
            ("thigh.L", "thigh.R"),
            
            # Bras gauche
            ("shoulder.L", "upper_arm.L"),
            ("upper_arm.L", "forearm.L"),
            
            # Bras droit
            ("shoulder.R", "upper_arm.R"),
            ("upper_arm.R", "forearm.R"),
            
            # Jambe gauche
            ("thigh.L", "shin.L"),
            ("shin.L", "foot.L"),
            
            # Jambe droite
            ("thigh.R", "shin.R"),
            ("shin.R", "foot.R"),
        ]
        
        # Variables pour l'animation
        self.current_frame = 0
        self.playing = False
        self.plotter = None

        # Analyser la plage des données
        self.min_val, self.max_val = self.analyze_data_range()
        
        # Calculer les limites d'affichage avec marge
        margin = 0.2
        self.display_range = [self.min_val - margin, self.max_val + margin]
        print(f"Plage d'affichage: [{self.display_range[0]:.3f}, {self.display_range[1]:.3f}]")
    
    def create_skeleton_for_frame(self, frame_nb):
        """Crée le squelette pour une frame donnée"""
        if frame_nb >= len(self.animation_data):
            return [], []
        
        frame_data = self.animation_data[frame_nb]
        
        # Extraire les positions des articulations
        joint_positions = {}
        for bone_name, bone_data in frame_data["bones"].items():
            if bone_data["visibility"] > 0.5:  # Filtrer les points peu visibles
                pos = bone_data["location"]
                joint_positions[bone_name] = [pos[0], pos[1], pos[2]]
        
        # Créer les sphères pour les articulations (taille adaptée)
        joint_objects = []
        for joint_name, position in joint_positions.items():
            sphere = Sphere(position, r=0.03, c='red')  # Taille réduite
            sphere.name = joint_name
            joint_objects.append(sphere)
        
        # Créer les lignes pour les os (épaisseur adaptée)
        bone_objects = []
        for start_bone, end_bone in self.bone_connections:
            if start_bone in joint_positions and end_bone in joint_positions:
                start_pos = joint_positions[start_bone]
                end_pos = joint_positions[end_bone]
                
                # Créer une ligne entre les deux points
                line = Line(start_pos, end_pos, c='cyan', lw=4)  # Couleur plus visible
                bone_objects.append(line)
        
        return joint_objects, bone_objects
    
    def setup_camera_and_bounds(self):
        """Configure la caméra et les limites d'affichage"""
        # Configurer les limites de la scène
        bounds = [self.display_range[0], self.display_range[1]] * 3  # x, y, z
        
        # Position optimale de la caméra
        center = [(self.max_val + self.min_val) / 2] * 3
        distance = (self.max_val - self.min_val) * 3  # Distance appropriée
        
        # Positionner la caméra
        camera_pos = [center[0] + distance, center[1] + distance, center[2] + distance]
        self.plotter.camera.SetPosition(camera_pos)
        self.plotter.camera.SetFocalPoint(center)
        self.plotter.camera.SetViewUp([0, 0, 1])  # Z vers le haut
    
    def on_key_press(self, event):
        """Gestionnaire d'événements clavier"""
        key = event.keyPressed
        
        if key == 'space' or key == 'Right':
            self.current_frame = (self.current_frame + 1) % len(self.animation_data)
            self.update_skeleton()
        elif key == 'Left':
            self.current_frame = (self.current_frame - 1) % len(self.animation_data)
            self.update_skeleton()
        elif key == 'r':
            self.current_frame = 0
            self.update_skeleton()
        elif key == 'p':
            self.playing = not self.playing
            print(f"Animation {'en cours' if self.playing else 'en pause'}")
        elif key == 'q' or key == 'Escape':
            self.plotter.close()
    
    def update_skeleton(self):
        """Met à jour l'affichage du squelette"""
        # Effacer les objets précédents (sauf les axes et grille)
        self.plotter.clear()
        
        # Reconfigurer la caméra après clear
        self.setup_camera_and_bounds()
        
        # Créer le squelette pour la frame actuelle
        joints, bones = self.create_skeleton_for_frame(self.current_frame)
        
        # Ajouter tous les objets à la scène
        for joint in joints:
            self.plotter.add(joint)
        
        for bone in bones:
            self.plotter.add(bone)
        
        # Ajouter une grille de référence
        grid_pos = [(self.max_val + self.min_val) / 2, 
                    (self.max_val + self.min_val) / 2, 
                    self.min_val - 0.1]
        grid_size = abs(self.max_val - self.min_val) * 1.5
        grid = Grid(pos=grid_pos, s=[grid_size, grid_size], c='gray', alpha=0.2)
        self.plotter.add(grid)
        
        # Texte pour le numéro de frame (position adaptée)
        text_pos = [self.min_val, self.min_val, self.max_val + 0.1]
        frame_text = Text3D(f"Frame: {self.current_frame + 1}/{len(self.animation_data)}", 
                           pos=text_pos, s=0.05, c='white')
        self.plotter.add(frame_text)
        
        # Instructions (position adaptée)
        instr_pos = [self.min_val, self.min_val, self.max_val - 0.1]
        instructions = Text3D("ESPACE/→: Suiv | ←: Prec | R: Début | Q: Quitter", 
                             pos=instr_pos, s=0.03, c='yellow')
        self.plotter.add(instructions)
        
        # Forcer la mise à jour
        self.plotter.render()
    
    def animate_interactive(self):
        """Animation interactive avec contrôles clavier"""
        self.plotter = Plotter(title="Animation Squelette 3D - Interactive", 
                              size=(1200, 800), axes=1)
        self.plotter.background('black')
        
        # Configuration initiale
        self.setup_camera_and_bounds()
        
        # Ajouter le gestionnaire d'événements
        self.plotter.add_callback('KeyPress', self.on_key_press)
        
        # Afficher la première frame
        self.update_skeleton()
        
        # Lancer la boucle interactive
        self.plotter.show(interactive=True)
    
    def animate_continuous(self, fps=20):
        """Animation continue automatique avec contrôles"""
        self.plotter = Plotter(title="Animation Squelette 3D - Continue (ESC pour quitter)", 
                              size=(1200, 800), axes=1)
        self.plotter.background('black')
        
        # Configuration initiale de la caméra
        self.setup_camera_and_bounds()
        
        # Variables pour l'animation
        frame_delay = 1.0 / fps
        start_time = time.time()
        
        # Gestionnaire pour quitter avec ESC
        def key_handler(event):
            if event.keyPressed in ['q', 'Escape']:
                self.plotter.close()
                return True
            return False
        
        self.plotter.add_callback('KeyPress', key_handler)
        
        # Boucle d'animation
        for frame_idx in range(len(self.animation_data)):
            loop_start = time.time()
            
            # Effacer les objets précédents
            self.plotter.clear()
            
            # Reconfigurer la caméra
            self.setup_camera_and_bounds()
            
            # Créer le squelette pour la frame actuelle
            joints, bones = self.create_skeleton_for_frame(frame_idx)
            
            # Ajouter tous les objets à la scène
            for joint in joints:
                self.plotter.add(joint)
            
            for bone in bones:
                self.plotter.add(bone)
            
            # Ajouter grille de référence
            grid_pos = [(self.max_val + self.min_val) / 2, 
                        (self.max_val + self.min_val) / 2, 
                        self.min_val - 0.1]
            grid_size = abs(self.max_val - self.min_val) * 1.5
            grid = Grid(pos=grid_pos, s=[grid_size, grid_size], c='gray', alpha=0.2)
            self.plotter.add(grid)
            
            # Texte pour le numéro de frame
            text_pos = [self.min_val, self.min_val, self.max_val + 0.1]
            frame_text = Text3D(f"Frame: {frame_idx + 1}/{len(self.animation_data)} | ESC: Quitter", 
                               pos=text_pos, s=0.05, c='white')
            self.plotter.add(frame_text)
            
            # Afficher la scène (mode interactif pour permettre les contrôles caméra)
            self.plotter.show(interactive=False, resetcam=False)
            
            # Gérer le timing
            loop_time = time.time() - loop_start
            remaining_time = frame_delay - loop_time
            if remaining_time > 0:
                time.sleep(remaining_time)
    
    def animate_with_timer(self, fps=20):
        """Animation avec timer Vedo - VERSION AMÉLIORÉE"""
        self.plotter = Plotter(title="Animation Squelette 3D - Timer", 
                              size=(1200, 800), axes=1)
        self.plotter.background('black')
        
        # Configuration initiale
        self.setup_camera_and_bounds()
        self.current_frame = 0
        
        def timer_callback(event):
            # Effacer et recréer
            self.plotter.clear()
            self.setup_camera_and_bounds()
            
            # Créer le squelette
            joints, bones = self.create_skeleton_for_frame(self.current_frame)
            
            for joint in joints:
                self.plotter.add(joint)
            for bone in bones:
                self.plotter.add(bone)
            
            # Grille et textes
            grid_pos = [(self.max_val + self.min_val) / 2, 
                        (self.max_val + self.min_val) / 2, 
                        self.min_val - 0.1]
            grid_size = abs(self.max_val - self.min_val) * 1.5
            grid = Grid(pos=grid_pos, s=[grid_size, grid_size], c='gray', alpha=0.2)
            self.plotter.add(grid)
            
            text_pos = [self.min_val, self.min_val, self.max_val + 0.1]
            frame_text = Text3D(f"Frame: {self.current_frame + 1}/{len(self.animation_data)}", 
                               pos=text_pos, s=0.05, c='white')
            self.plotter.add(frame_text)
            
            # Passer à la frame suivante
            self.current_frame = (self.current_frame + 1) % len(self.animation_data)
            
            self.plotter.render()
        
        # Gestionnaire clavier
        def key_handler(event):
            if event.keyPressed in ['q', 'Escape']:
                self.plotter.close()
        
        # Ajouter les callbacks
        self.plotter.add_callback('timer', timer_callback)
        self.plotter.add_callback('KeyPress', key_handler)
        
        # Démarrer le timer
        self.plotter.timer_callback('create', dt=int(1000/fps))
        
        # Afficher la première frame
        timer_callback(None)
        
        # Lancer l'animation
        self.plotter.show(interactive=True)
    
    def show_single_frame(self, frame_idx=0):
        """Affiche une seule frame pour tester"""
        self.plotter = Plotter(title="Animation Squelette 3D - Frame statique", 
                              size=(1200, 800), axes=1)
        self.plotter.background('black')
        
        # Configuration de la caméra
        self.setup_camera_and_bounds()
        
        joints, bones = self.create_skeleton_for_frame(frame_idx)
        
        # Ajouter tous les objets à la scène
        for joint in joints:
            self.plotter.add(joint)
        
        for bone in bones:
            self.plotter.add(bone)
        
        # Grille de référence
        grid_pos = [(self.max_val + self.min_val) / 2, 
                    (self.max_val + self.min_val) / 2, 
                    self.min_val - 0.1]
        grid_size = abs(self.max_val - self.min_val) * 1.5
        grid = Grid(pos=grid_pos, s=[grid_size, grid_size], c='gray', alpha=0.2)
        self.plotter.add(grid)
        
        # Texte
        text_pos = [self.min_val, self.min_val, self.max_val + 0.1]
        frame_text = Text3D(f"Frame: {frame_idx + 1}/{len(self.animation_data)}", 
                           pos=text_pos, s=0.05, c='white')
        self.plotter.add(frame_text)
        
        # Afficher la scène de manière interactive
        self.plotter.show()
        
    def analyze_data_range(self):
        """Analyse la plage des données pour optimiser l'affichage"""
        all_positions = []
        
        for frame_data in self.animation_data:
            for bone_name, bone_data in frame_data["bones"].items():
                if bone_data["visibility"] > 0.5:
                    pos = bone_data["location"]
                    all_positions.extend(pos)
        
        if all_positions:
            min_val = min(all_positions)
            max_val = max(all_positions)
            print(f"Plage des données: [{min_val:.3f}, {max_val:.3f}]")
            return min_val, max_val
        return -1, 1

if __name__ == "__main__":
    try:
        # Trouver le fichier d'animation le plus récent
        import os
        json_files = [f for f in os.listdir('.') if f.startswith('animation_data_') and f.endswith('.json')]
        
        if not json_files:
            print("Aucun fichier d'animation trouvé!")
            print("Assurez-vous d'avoir un fichier 'animation_data_XXXXXXXX_XXXXXX.json'")
            exit(1)
        
        json_file = sorted(json_files)[-1]
        print(f"Utilisation du fichier: {json_file}")
        
        # Créer l'animateur
        animator = SkeletonAnimatorVedo(json_file)
        
        # Menu de choix
        print("\nOptions d'animation:")
        print("1. Afficher une frame statique (test)")
        print("2. Animation interactive (contrôles clavier)")
        print("3. Animation continue automatique")
        print("4. Animation avec timer (boucle automatique)")
        
        choice = input("Choisissez une option (1-4): ").strip()
        
        if choice == "1":
            frame_num = input(f"Numéro de frame à afficher (1-{len(animator.animation_data)}): ")
            try:
                frame_idx = int(frame_num) - 1
                if 0 <= frame_idx < len(animator.animation_data):
                    animator.show_single_frame(frame_idx)
                else:
                    print("Numéro de frame invalide!")
            except ValueError:
                print("Veuillez entrer un nombre valide!")
                
        elif choice == "2":
            print("Contrôles:")
            print("  ESPACE/→: Frame suivante")
            print("  ←: Frame précédente") 
            print("  R: Retour au début")
            print("  Q/ESC: Quitter")
            animator.animate_interactive()
            
        elif choice == "3":
            fps = input("FPS d'animation (défaut: 20): ").strip()
            try:
                fps = int(fps) if fps else 20
                animator.animate_continuous(fps=fps)
            except ValueError:
                animator.animate_continuous(fps=20)
                
        elif choice == "4":
            fps = input("FPS d'animation (défaut: 10): ").strip()
            try:
                fps = int(fps) if fps else 10
                animator.animate_with_timer(fps=fps)
            except ValueError:
                animator.animate_with_timer(fps=10)
        else:
            print("Option non reconnue, affichage de la première frame...")
            animator.show_single_frame(0)
            
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()