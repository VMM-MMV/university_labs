def stalinSort(data):
  for i in range(len(data) - 1):
    if data[i] > data[i + 1]:
      del data[i + 1]

  return data
