# Base image 
FROM python:3.12-bookworm

# Update packages and install necessary packets
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash=5.2.15-2+b7 \
    build-essential=12.9 \
    meson=1.0.1-5\
    nasm=2.16.01-1\
    yasm=1.3.0-4\
    git=1:2.39.5-0+deb12u2\
    python3-dev=3.11.2-1+b1\
    gcc=4:12.2.0-3\
    libtool=2.4.7-7~deb12u1\
    libpng-dev=1.6.39-2\
    libjpeg-dev=1:2.1.5-2\
    zlib1g-dev=1:1.2.13.dfsg-1\
    linux-headers-amd64\  
    vim=2:9.0.1378-2+deb12u2\
    nano=7.2-1+deb12u1\
    libx264-dev=2:0.164.3095+gitbaee400-3\
    libx265-dev=3.5-2+b1\
    libvpx-dev=1.12.0-1+deb12u3\
    libvorbis-dev=1.3.7-1\
    libopus-dev=1.3.1-3\
    libaom-dev=3.6.0-1+deb12u1\
    xxd=2:9.0.1378-2+deb12u2\
    cmake=3.25.1-1\
    clang-tidy=1:14.0-55.7~deb12u1\
    clang-format=1:14.0-55.7~deb12u1
   

# Python libraries for analysis and graphs
RUN pip3 install matplotlib==3.9.2 numpy==2.1.1 pandas==2.2.3 scipy==1.14.1



# Download the zip of VMAF (version 3.0.0) and install libvmaf
RUN curl -L https://github.com/Netflix/vmaf/archive/refs/tags/v3.0.0.zip -o vmaf.zip \
    && unzip vmaf.zip \
    && cd vmaf-3.0.0/libvmaf \
    #&& meson build --buildtype release \
    && meson setup build --buildtype release -Denable_float=true \ 
    ##option needed to run float models
    && ninja -C build \
    && ninja -C build install


# Download the zip of FFmpeg version 7.0.2 and compile with the correct options
RUN curl -L https://github.com/FFmpeg/FFmpeg/archive/refs/tags/n7.0.2.zip -o ffmpeg.zip \
    && unzip ffmpeg.zip \
    && cd FFmpeg-n7.0.2 \
    && ./configure --enable-gpl  --enable-libvmaf --enable-libx264 --enable-libx265 --enable-libaom --enable-libvpx --enable-libvorbis --enable-libopus \
    && make -j$(nproc) \
    && make install \
    && ldconfig  


#Download the ZIP of the ESSIM Git repository, with the version fixed to a specific commit.
RUN curl -L https://github.com/facebookresearch/essim/archive/4131785b1fe2b920af9c698066fde79df76982b8.zip -o essim.zip \
    && unzip essim.zip \
    && mv essim-4131785b1fe2b920af9c698066fde79df76982b8 /essim \  
    && cd /essim \
    && mkdir build \
    && cd build \
    && cmake .. -G Ninja \
    && cmake --build . --parallel


# Create a directory for videos,results and hash
RUN mkdir -p /reference /distorted /results /hash /mos

# Set the working directory
WORKDIR /app

# Copy scripts

COPY run_experiments.sh .

# Make scripts executable
RUN chmod +x run_experiments.sh 

CMD ["/bin/sh"]