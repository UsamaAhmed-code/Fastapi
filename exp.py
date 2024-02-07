


two_d_array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten the 2D array into a 1D array
one_d_array = [item for sublist in two_d_array for item in sublist]

print(one_d_array)
