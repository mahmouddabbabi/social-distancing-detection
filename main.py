def main():
	"""
	Perform Object detection
	"""
	
	configPath = "./detection_files/yolov3.cfg"
	weightPath = "./detection_files/yolov3.weights"
	metaPath = "./detection_files/coco.data"

	netMain = darknet.load_net_custom(configPath.encode(
			"ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
	metaMain = darknet.load_meta(metaPath.encode("ascii"))
	try:
		with open(metaPath) as metaFH:
			metaContents = metaFH.read()
			import re
			match = re.search("names *= *(.*)$", metaContents,
							  re.IGNORECASE | re.MULTILINE)
			if match:
				result = match.group(1)
			else:
				result = None
			try:
				if os.path.exists(result):
					with open(result) as namesFH:
						namesList = namesFH.read().strip().split("\n")
						altNames = [x.strip() for x in namesList]
			except TypeError:
				pass
	except Exception:
		pass


	cap = cv2.VideoCapture("./Video.mp4")


	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	

	new_height = frame_height // 2
	new_width  = frame_width // 2

	out = cv2.VideoWriter("./outout/output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,(new_width, new_height))
	

	darknet_image = darknet.make_image(new_width, new_height, 3)
	
	while True:
		prev_time = time.time()
		ret, frame_read = cap.read()


		if not ret:
			break

		frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
		frame_resized = cv2.resize(frame_rgb,
								   (new_width, new_height),
								   interpolation=cv2.INTER_LINEAR)

		darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

		detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
		
		image = cvDrawBoxes(detections, frame_resized)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		
		print(1/(time.time()-prev_time))
		
		cv2.imshow('Demo', image)
		
		cv2.waitKey(3)

		out.write(image)

	cap.release()


	out.release()

if __name__ == "__main__":
	main()