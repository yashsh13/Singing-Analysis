import librosa
import numpy as np

def analysis(audio_path):

    #Get amplitude and sampling rate from audio
    amplitude, sr = librosa.load(audio_path,sr=None)

    #Get frequency
    frequency, voiced_flag, voiced_prob = librosa.pyin(
    amplitude,
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7'),
    )

    frequency[voiced_flag<0.7] = np.nan

    #First parameter pitch mean
    pitch_mean = np.nanstd(frequency)

    #Second parameter pitch standard deviation
    pitch_std = np.nanstd(frequency)

    #Third parameter pitch range 
    pitch_range = np.nanmax(frequency) - np.nanmin(frequency)

    #Fourth parameter pitch variation with time 
    valid_index = ~(np.isnan(frequency))
    x = np.arange(len(frequency))[valid_index]
    y = frequency[valid_index]

    pitch_slope_wrt_time = np.polyfit(x,y,1)[0]

    #Calculating onset envelope strenght mean
    onset_env = librosa.onset.onset_strength(y=amplitude,sr=sr)
    onset_strength_mean = np.mean(onset_env)
    

    #Calculating Tempo and note duration mean
    tempo, onset_times = librosa.beat.beat_track(onset_envelope = onset_env, sr=sr,units='time')

    note_durations = np.diff(onset_times)
    note_duration_mean = np.mean(note_durations)
    note_duration_std = np.std(note_durations)

    parameters = {
        'pitch mean': pitch_mean,
        'pitch std': pitch_std,
        'pitch range': pitch_range,
        'pitch variation wrt time': pitch_slope_wrt_time,
        'onset strength mean': onset_strength_mean,
        'tempo': tempo,
        'note duration mean': note_duration_mean,
        'note duration std': note_duration_std 
    }

    return parameters









