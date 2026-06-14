import struct
import winsound
import math

def play_beep():
    notes = [
        (440, 500),  # A4
        (494, 500),  # B4
        (523, 500),  # C5
        (587, 500),  # D5
        (659, 500),  # E5
    ]
    for frequency, duration in notes:
        winsound.Beep(frequency, duration)

def play_system_sound():
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

def play_sound(frequencies = [(440, 1), (442, 1), (445, 1)], duration_sec = 5.0):

    SAMPLE_RATE = 44100
    CHANNELS = 1
    TOTAL_SAMPLES = int(SAMPLE_RATE * duration_sec)
    
    # FREQUENCIES = [440, 442, 445]

    pcm_bytes = bytearray()

    for i in range(TOTAL_SAMPLES):
        t = i / SAMPLE_RATE
        
        # Simple linear envelope (quick fade in, long hold, quick fade out)
        if t < 0.1:
            volume = t / 0.1
        elif t > (duration_sec - 0.5):
            volume = (duration_sec - t) / 0.5
        else:
            volume = 1.0
        
        # Normalize by the number of frequencies to stay within strict limits (-1.0 to 1.0) and apply master volume and pack into 16-bit signed integer format
        normalized_wave = (sum([f[1] * math.sin(2 * math.pi * f[0] * t) for f in frequencies]) / len(frequencies)) * volume
        integer_sample = int(normalized_wave * 32767)
        pcm_bytes.extend(struct.pack("<h", integer_sample))

    # Assemble standard Windows WAV file container structures
    total_data_size = len(pcm_bytes)
    total_file_size = 44 + total_data_size
    wav_header = (
        b"RIFF" + struct.pack("<I", total_file_size - 8) + b"WAVEfmt " +
        struct.pack("<IHHIIHH", 16, 1, CHANNELS, SAMPLE_RATE, SAMPLE_RATE * 2, 2, 16) +
        b"data" + struct.pack("<I", total_data_size)
    )

    print("Playing triple-frequency phase beating stream...")
    winsound.PlaySound(wav_header + pcm_bytes, winsound.SND_MEMORY)
    print("Finished!")

def get_harmonic_frequencies(base_freq, num_harmonics):
    return [(base_freq * (i + 1), 1 / (i + 1)) for i in range(num_harmonics)]

# play_beep()
# play_system_sound
play_sound(get_harmonic_frequencies(230, 11))