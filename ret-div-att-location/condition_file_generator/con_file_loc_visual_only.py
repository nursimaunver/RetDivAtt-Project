import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from IPython.display import display
import random 


# this function enables us to add 'objects/' string before the file names
def add_string(word, string_arr):
	
	for k in range(string_arr.shape[0]):

		string_arr[k] = str(word) + str(string_arr[k])

	return (string_arr)


def listdir_ignore_hidden(path):
	"""

	It excludes the hidden files from the listdir()

	"""
	files = os.listdir(path)

	new_files = []

	for file in files:

		if not file.startswith("."):

			new_files.append(file)

	return new_files


def generate_circle_random(n=32, r=0.4, x0=0, y0=0):
	t = np.linspace(0, 2 * np.pi, n+1) # select n angles from 0 to 360
	random_angle = np.random.uniform(low=0, high=np.pi*2) 
	t += random_angle  # add a random angle to the previous angle, the space between the angles will remain the same 
	px = x0 + r*np.cos(t)
	py = y0 + r*np.sin(t)

	px = px[:-1] # remove the last one so that it gives different values -sonuncuyu atmak için -aynı değerler olmasın-
	py = py[:-1]

	#plt.scatter(px, py)
	#plt.show()
	return px, py


def generate_orientation(n=40): #generate orientations from -178 to + 180 with 2 degree difference

	orientation_option = [-45, -30, -15, 15, 30, 45]

	orientation_list = np.random.choice(orientation_option, size=n)

	return orientation_list

def generate_condition_file(object_paths, object_folder_paths, condition_filename, side_selection):
	number_of_objects=object_paths.shape[0]
	objects_x, objects_y= generate_circle_random(number_of_objects)
	# Fetch files
	
	sound_files = np.array(listdir_ignore_hidden("./sounds/"))  #creates an array for the sound files(50) 
	
	
	distractor_folders_path= "./distractor_folders/"
	distractor_folders=np.array(listdir_ignore_hidden(distractor_folders_path), dtype= np.str) #includes sub-folders of distractor_folders
	distractor_selected=np.empty((number_of_objects,12),dtype=object) #initialize distractors array

	for k in range(number_of_objects): #for each row(object) we create 12 distractors

		np.random.shuffle(distractor_folders)
		for m in range(12):

		#for distractor_folder in distractor_folders[:12]:
			distractor_folder= distractor_folders[m] #abacus-folder
			distractor_folder_path = distractor_folders_path + distractor_folder # distractor_folders/abacus 
			distractor_files= np.array(listdir_ignore_hidden(distractor_folder_path),dtype=object) #abacus1.png...
			distractor_selected[k,m]=os.path.join(distractor_folder_path,  np.random.choice(distractor_files)) #distractor_folders/abacus/abacus1.png


	object_selected=np.empty((number_of_objects,),dtype=object) #initialize object selected

	for k in range(number_of_objects):

		object_folder_path = object_folder_paths[k] #selects one folder from object_folders with its path
		object_files= np.array(listdir_ignore_hidden(object_folder_path),dtype=object) #selects all files from the selected folder 
		object_selected[k]=os.path.join(object_folder_path,  np.random.choice(object_files)) #selects one file from all files of the selected folder

	# define distractor locations

	dist_x= [0.4,-0.4,0.18,-0.18,-0.35,0.35,-0.28,0.28,-0.37,0.37,-0.23,0.23]
	dist_y= [0.0,0.0,-0.35,-0.35, 0.18,0.18,-0.28,-0.28,-0.15,-0.15,0.32,0.32]

	dist_px_py = np.vstack([ dist_x, dist_y]).T


	# Shuffle the study section
	np.random.shuffle(dist_px_py)
	dist_locations= dist_px_py[:number_of_objects]





	# Filler Task
	filler_task_number = 50 #number of the task -> N
	filler_choice_number = 50 #number of trials
	nums1 = np.random.randint(1, 11, size=(filler_choice_number,))
	nums2 = np.random.randint(1, 11, size=(filler_choice_number,))
	ops = np.random.choice(["+", "-", "x"], size=(filler_choice_number,))

	num1_op_num2 = []

	counter = 0

	for k in range(filler_choice_number): #create mathematical operations as a filler task

		if (nums2[k] > nums1[k]) and (ops[k] == "-"):

			continue

		else:

			num1_op_num2.append(str(nums1[k]) + str(ops[k]) + str(nums2[k]))
			counter += 1

		if counter == filler_task_number:

			break



	sound_files_selected = np.random.choice(sound_files, number_of_objects)



	condition = True

	cnt = 0
	while condition:

	
		rand_ix = np.random.randint(0, 2, size = (number_of_objects, ))

		#print(rand_ix[rand_ix == 0].shape[0])
		#print(rand_ix[rand_ix == 1].shape[0])
		#print(rand_ix[rand_ix == 2].shape[0])

		condition = not(rand_ix[rand_ix == 0].shape[0] == rand_ix[rand_ix == 1].shape[0]  == number_of_objects / 2)
		cnt += 1
		print("{}. trial, situation is {}".format(cnt, not condition))



	arr = np.zeros((number_of_objects, 2))

	for k in range(number_of_objects):

		arr[k][rand_ix[k]] = 1

	print(arr)





	cor_ans= []
	cor_ans_dist= []
	res = [int(sub.split('.')[0]) for sub in sound_files_selected]
	if side_selection == "assa":

		#odd is "s" version 
		for i in range(len(res)):
			if res[i] % 2 == 0:
				cor_ans.append('a')
			else:
				cor_ans.append('s')
		#s in the left version 
		for m in range(len(dist_locations)):
			if dist_locations[m,0]<0:
				cor_ans_dist.append('s')
			else:
				cor_ans_dist.append('a')
	elif side_selection == "saas":

		#odd is "a" version 
		for i in range(len(res)):
			if res[i] % 2 == 0:
				cor_ans.append('s')
			else:
				cor_ans.append('a')
		#a in the left version 
		for m in range(len(dist_locations)):
			if dist_locations[m,0]<0:
				cor_ans_dist.append('a')
			else:
				cor_ans_dist.append('s') 
	else:
		print("Please choose assa or saas")

	# DataFrame writing to excel
	general_dict = {"objects": add_string("objects/", object_paths),
					"objects_location_x": objects_x,
					"objects_location_y": objects_y,
					"dist_location_x": dist_locations[:, 0],
					"dist_location_y": dist_locations[:, 1],
					"orientation_array": generate_orientation(number_of_objects),
					"auso": sound_files_selected,
					"calc": num1_op_num2,
					"base_rep" : arr[:,0], "dist_rep": arr[:,1],
					"correct_ans_sound":cor_ans,
					"correct_ans_dist" :cor_ans_dist,
					**{"dist{}".format(k):distractor_selected[:,k] for k in range(12)},
					"objects_new": object_selected}

	general_file = pd.DataFrame.from_dict(general_dict, orient="index").transpose()
	general_file["auso"] = "sounds/" + general_file["auso"]
	#general_file.reset_index(drop=True, inplace=True)
	general_file.to_excel(condition_filename, index=False)



if __name__ == "__main__": #
	
	object_files = np.array(listdir_ignore_hidden("./objects/"))
	object_folder_paths = add_string("./object_folders/", np.array(listdir_ignore_hidden("./object_folders/"), dtype=object))
	np.random.shuffle(object_folder_paths)
	number_of_objects=6

	for (idx,k) in enumerate(range(0, object_files.shape[0],number_of_objects)): # k goes from 0 to 240 by 6, idx counts the number of 6's. in the end it creates 6x40 condition files
		generate_condition_file(object_files[k:k+number_of_objects], object_folder_paths[k:k+number_of_objects], "{}.xlsx".format(idx),side_selection="saas")
