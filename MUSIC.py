import numpy as np
import soundfile as sf
from scipy.linalg import eigh

def load_wav_file(filename):
    """
    读取多通道wav文件。
    """
    data, samplerate = sf.read(filename)
    return data, samplerate

def compute_steering_vector(mic_positions, angle, frequency, speed_of_sound=343):
    """
    计算导向矢量。
    """
    wavelength = speed_of_sound / frequency
    k = 2 * np.pi / wavelength
    steering_vector = np.exp(-1j * k * (mic_positions @ [np.cos(angle), np.sin(angle)]))
    return steering_vector

def music_doa_estimation(mic_signals, mic_positions, scan_angles, num_sources, frequency, speed_of_sound=343):
    """
    使用MUSIC方法进行DOA估计。
    """
    M, N = mic_signals.shape
    L = len(scan_angles)

    # 计算协方差矩阵 R
    R = np.dot(mic_signals, mic_signals.conj().T) / N

    # 特征值分解
    eigvals, eigvecs = eigh(R)
    idx = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, idx]

    # 信号子空间和噪声子空间
    signal_subspace = eigvecs[:, :num_sources]
    noise_subspace = eigvecs[:, num_sources:]

    # 预先计算导向矢量
    steering_vectors = np.zeros((M, L), dtype=complex)
    for i, angle in enumerate(scan_angles):
        steering_vectors[:, i] = compute_steering_vector(mic_positions, angle, frequency, speed_of_sound)

    # 计算MUSIC谱
    music_spectrum = np.zeros(L)
    for i in range(L):
        a_theta = steering_vectors[:, i]
        music_spectrum[i] = 1 / np.real(np.dot(a_theta.conj().T, np.dot(noise_subspace, np.dot(noise_subspace.conj().T, a_theta))))

    # 找到谱峰值对应的角度
    doa_index = np.argmax(music_spectrum)
    doa_angle = scan_angles[doa_index]

    return doa_angle

# 示例使用
if __name__ == "__main__":
    # 加载音频文件
    filename = 'test.wav'
    data, samplerate = load_wav_file(filename)

    # 麦克风位置（圆形阵列，半径0.05米）
    radius = 0.05
    mic_positions = np.array([
        [radius * np.cos(theta), radius * np.sin(theta)]
        for theta in np.linspace(0, 2 * np.pi, 4, endpoint=False)
    ])

    # 要扫描的角度范围（从-90度到90度）
    scan_angles = np.linspace(-np.pi/2, np.pi/2, 180)

    # 假设有一个信号源
    num_sources = 1

    # 帧长和帧移
    frame_length = 512
    frame_shift = 256  # 可以调整帧移大小

    # 频率选择（假设使用中心频率）
    frequency = 1000  # 可以根据实际情况调整

    # 对每一帧进行DOA估计
    num_frames = (data.shape[0] - frame_length) // frame_shift + 1
    estimated_doas = []

    for i in range(num_frames):
        start_idx = i * frame_shift
        end_idx = start_idx + frame_length
        frame_data = data[start_idx:end_idx, :].T  # 转置以匹配 (M, N) 形状

        # 进行DOA估计
        estimated_doa = music_doa_estimation(frame_data, mic_positions, scan_angles, num_sources, frequency)
        estimated_doas.append(np.degrees(estimated_doa))

    # 打印结果
    for i, doa in enumerate(estimated_doas):
        print(f"Frame {i}: Estimated DOA = {doa:.2f} degrees")