import React, { useEffect, useRef } from 'react';
import io from 'socket.io-client';
import Peer from 'simple-peer';

const socket = io('http://localhost:8000');
const ICE_SERVERS = [
  { urls: 'stun:stun.l.google.com:19302' },
  {
    urls: 'turn:你的TURN服务器IP:3478',
    username: 'username',
    credential: 'password'
  }
];

function App() {
  const localVideoRef = useRef();
  const remoteVideoRef = useRef();
  const peerRef = useRef();

  // 初始化媒体设备
  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        localVideoRef.current.srcObject = stream;
      });
  }, []);

  // 处理 WebRTC 连接
  const startCall = () => {
    const peer = new Peer({
      initiator: true,
      trickle: true,
      config: { iceServers: ICE_SERVERS }
    });

    peer.on('signal', data => {
      socket.emit('offer', {
        sdp: data,
        targetId: 'digital_human'
      });
    });

    peer.on('stream', stream => {
      remoteVideoRef.current.srcObject = stream;
    });

    peerRef.current = peer;
  };

  return (
    <div>
      <video ref={localVideoRef} autoPlay muted />
      <video ref={remoteVideoRef} autoPlay />
      <button onClick={startCall}>开始对话</button>
    </div>
  );
}

export default App;