import numpy as np

def generate_possible_jobs(style, df_jobs, stat_cols):

	valid_jobs = []
	
	if style == "Meteor":
		for idx1, job1 in df_jobs[stat_cols].iterrows():
			for idx2, job2 in df_jobs[stat_cols].iterrows():
				for idx3, job3 in df_jobs[stat_cols].iterrows():
					for idx4, job4 in df_jobs[stat_cols].iterrows():
						
						party_index = ",".join([idx1, idx2, idx3, idx4])
						party_embedding = np.concatenate((job1.to_numpy(), job2.to_numpy(), job3.to_numpy(), job4.to_numpy()))
						valid_jobs.append((party_index, party_embedding))
	else:
		raise ValueError(f"Bad game style {style}.")

	return valid_jobs
