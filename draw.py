from numerical import convert , distance

def draw(detections, img):

	if len(detections) > 0:  						  
		
		centroid_dict = {} 						
		
		objectId = 0								
		
		for detection in detections:				
			
			name_tag = str(detection[0].decode())   
			if name_tag == 'person':                
				x, y, w, h = detection[2][0],detection[2][1],detection[2][2],detection[2][3]      	
				
				xmin, ymin, xmax, ymax = convert(float(x), float(y), float(w), float(h))   
				


				centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) 
				
				objectId += 1      

			
		red_zone_list = [] 
		red_line_list = []
		for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2): 
			dx, dy = p1[0] - p2[0], p1[1] - p2[1]  	
			distance = distance(dx, dy) 			
			if distance < 75.0:						
				if id1 not in red_zone_list:
					red_zone_list.append(id1)       
					red_line_list.append(p1[0:2])   
				if id2 not in red_zone_list:
					red_zone_list.append(id2)		 
					red_line_list.append(p2[0:2])
		
		for idx, box in centroid_dict.items(): 
			if idx in red_zone_list:   
				cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) 
			else:
				cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) 


	   
		text = "People at Risk: %s" % str(len(red_zone_list)) 			
		location = (10,25)												
		cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (246,86,86), 2, cv2.LINE_AA)  

		for check in range(0, len(red_line_list)-1):					
			start_point = red_line_list[check] 
			end_point = red_line_list[check+1]
			check_line_x = abs(end_point[0] - start_point[0])   		  
			check_line_y = abs(end_point[1] - start_point[1])			
			if (check_line_x < 75) and (check_line_y < 25):				
				cv2.line(img, start_point, end_point, (255, 0, 0), 2)    



	return img


