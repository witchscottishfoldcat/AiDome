# main.gd (Corrected for Godot 4.x)

extends Node2D

# --- 1. 定义核心变量 ---
# “大脑”服务的地址保持不变
const BRAIN_URL = "ws://127.0.0.1:8000/ws/v1/godot_body_1"

# 在Godot 4中，我们使用 WebSocketPeer 来处理连接
var _peer: WebSocketPeer
# 添加一个状态变量，确保我们的“问好”消息只发送一次
var _is_connected = false


# --- 2. 引擎入口函数：当节点准备好时执行 ---
func _ready():
	"""
	Godot 4的启动函数。
	任务：创建Peer实例，并发起连接。
	"""
	print("Body Prototype (Godot 4): Initializing...")
	
	# 步骤A: 创建WebSocketPeer实例
	_peer = WebSocketPeer.new()
	
	# 步骤B: 尝试连接到“大脑”服务
	var err = _peer.connect_to_url(BRAIN_URL)
	if err != OK:
		print("Body Prototype: Unable to initiate connection. Error code: ", err)


# --- 3. 引擎循环函数：每一帧都执行 ---
func _process(delta):
	"""
	在Godot 4中，所有网络事件的处理都通过在 _process 中轮询(poll)Peer来完成。
	我们需要在这里检查连接状态和接收数据。
	"""
	# 如果peer不存在或未连接，则不执行任何操作
	if not _peer:
		return
		
	# 必须每帧调用poll来处理网络数据包
	_peer.poll()
	
	# 获取当前的连接状态
	var state = _peer.get_ready_state()
	
	if state == WebSocketPeer.STATE_OPEN:
		# --- 连接已成功打开 ---
		
		# 如果这是我们第一次检测到连接成功
		if not _is_connected:
			_is_connected = true
			print("Body Prototype: Connection ESTABLISHED!")
			# 发送我们的测试问候消息
			_peer.send_text("Hello Brain, this is the Body.")
		
		# 循环检查是否有新的数据包到达
		while _peer.get_available_packet_count() > 0:
			var received_json_string = _peer.get_packet().get_string_from_utf8()
			print("Body Prototype: Data RECEIVED from Brain: ", received_json_string)

	elif state == WebSocketPeer.STATE_CLOSING:
		# --- 服务器或我们正在关闭连接 ---
		pass # 可以在这里添加日志
		
	elif state == WebSocketPeer.STATE_CLOSED:
		# --- 连接已彻底关闭 ---
		var code = _peer.get_close_code()
		var reason = _peer.get_close_reason()
		print("Body Prototype: Connection CLOSED with code: %d, reason: %s" % [code, reason])
		# 停止进一步处理，可以禁用此节点的process循环
		set_process(false)
func _input(event):
	if event is InputEventKey and event.pressed:
		var custom_message = "今天天气真好"
		if _is_connected:
			_peer.send_text(custom_message)
			print("Body Prototype: Manually sent message: ", custom_message)
