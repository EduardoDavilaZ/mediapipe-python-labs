import pygame
import os
import numpy as np
import config.config as settings

class AudioEngine:
    """
    Manages the loading, pitch-shifting, and playback of piano note samples.
    Uses numpy for real-time resampling to generate chromatic notes from 
    a limited set of base samples.
    """
    def __init__(self):
        # Initialize pygame mixer with custom audio settings
        pygame.mixer.pre_init(settings.SAMPLE_RATE, -16, 2, settings.BUFFER_SIZE)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(64)
        
        # Mapping for Octaves 3, 4, and 5
        # Pitch mapping: (filename, semitone_shift)
        # Shift values: -1 (Down), 0 (Original), 1 (Up)
        self.pitch_map = {
            # OCTAVE 3
            "C3": ("C3v15.flac", 0), "C#3": ("C3v15.flac", 1),
            "D3": ("D#3v15.flac", -1), "D#3": ("D#3v15.flac", 0), "E3": ("D#3v15.flac", 1),
            "F3": ("F#3v15.flac", -1), "F#3": ("F#3v15.flac", 0), "G3": ("F#3v15.flac", 1),
            "G#3": ("A3v15.flac", -1), "A3": ("A3v15.flac", 0), "A#3": ("A3v15.flac", 1),
            "B3": ("C4v15.flac", -1),

            # OCTAVE 4
            "C4": ("C4v15.flac", 0), "C#4": ("C4v15.flac", 1),
            "D4": ("D#4v15.flac", -1), "D#4": ("D#4v15.flac", 0), "E4": ("D#4v15.flac", 1),
            "F4": ("F#4v15.flac", -1), "F#4": ("F#4v15.flac", 1), "G4": ("F#4v15.flac", 1),
            "G#4": ("A4v15.flac", -1), "A4": ("A4v15.flac", 0), "A#4": ("A4v15.flac", 1),
            "B4": ("C5v15.flac", -1),

            # OCTAVE 5
            "C5": ("C5v15.flac", 0), "C#5": ("C5v15.flac", 1),
            "D5": ("D#5v15.flac", -1), "D#5": ("D#5v15.flac", 0), "E5": ("D#5v15.flac", 1),
            "F5": ("F#5v15.flac", -1), "F#5": ("F#5v15.flac", 0), "G5": ("F#5v15.flac", 1),
            "G#5": ("A5v15.flac", -1), "A5": ("A5v15.flac", 0), "A#5": ("A5v15.flac", 1),
            "B5": ("C6v15.flac", -1)
        }
        
        self.sounds = self._load_pitched_samples()

    def _load_pitched_samples(self):
        """
        Loads base FLAC samples and generates pitch-shifted versions 
        using array resampling.
        """
        loaded_sounds = {}
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sounds_path = os.path.join(base_path, "assets", "sounds")

        print("Generating notes via pitch shifting...")

        for note, (file_name, semi_shift) in self.pitch_map.items():
            full_path = os.path.join(sounds_path, file_name)
            
            if os.path.exists(full_path):
                try:
                    orig_sound = pygame.mixer.Sound(full_path)
                    
                    if semi_shift == 0:
                        loaded_sounds[note] = orig_sound
                    else:
                        # Convert sound data to numpy array for processing
                        sound_array = pygame.sndarray.array(orig_sound)
                        
                        # Pitch shift factor calculation: 2^(n/12)
                        factor = 2 ** (semi_shift / 12.0)
                        
                        # Resample array to achieve target pitch
                        new_indices = np.arange(0, len(sound_array), factor)
                        new_indices = new_indices[new_indices < len(sound_array)].astype(int)
                        new_array = sound_array[new_indices]
                        
                        # Convert processed array back to a playable Sound object
                        loaded_sounds[note] = pygame.sndarray.make_sound(new_array)
                except Exception as e:
                    print(f"Error processing {note}: {e}")
            else:
                print(f"Alert: Base file {file_name} not found for note {note}")
        
        print(f"Piano ready: {len(loaded_sounds)} notes configured.")
        return loaded_sounds

    def play(self, note_name):
        """
        Plays the requested note if it exists in the loaded sounds dictionary.
        Applies a fadeout effect to create a more natural sustain.
        """
        sound = self.sounds.get(note_name)
        if sound:
            sound.set_volume(1)
            channel = sound.play()
            if channel:
                channel.fadeout(settings.FADE_OUT_MS)