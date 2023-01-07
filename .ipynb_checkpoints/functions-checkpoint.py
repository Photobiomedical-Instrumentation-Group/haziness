import numpy as np


def Michelson(image):
    """
    Michelson metric.

    Parameters
    ----------
    image : array
        Image to apply the metric

    Returns
    ----------
    float
        Value of the metric
    """
    if type(image) == np.ndarray:
        image = image 
    maximo = int(np.max(image))
    minimo = int(np.min(image))
    
    numerator = maximo - minimo
    denominator = maximo + minimo
    
    # Avoids division by zero
    if denominator == 0:
        denominator = 1
    
    return numerator/denominator
  
def RMS(image):
    """
    RMS metric.

    Parameters
    ----------
    image : array
        Image to apply the metric

    Returns
    ----------
    float
        Value of the metric
    """
    if type(image) == str:
        image = cv2.imread(image,0) 
    elif type(image) == np.ndarray:
        image = image # NÃO NECESSARIAMENTE PRETO E BRANCO
#     image = cv2.imread(image,0)
    image = image/255
    x,y = image.shape
    LM = x * y
    Imed = np.sum(image)/LM
    sum1 = (image - Imed)**2
    sum2 = np.sum(sum1)
    
    
    return np.sqrt(sum2/LM)

def HS(image):
    """
    Histogram spread metric.

    Parameters
    ----------
    image : array
        Image to apply the metric

    Returns
    ----------
    float
        Value of the metric
    """
    
    # Number of pixels for each intensity
    count, _ = np.histogram(image, bins=256, range=[0, 256])

    histo = count / sum(count) # Normalizing

    cumulative  = np.cumsum(count) # Cumulative histogram
    # Normalizing the cumulative histogram
    normcum = (cumulative - min(cumulative))/(max(cumulative)-min(cumulative))
    
    # Closest position to the quartils
    value1 = np.where(normcum == min(normcum, key=lambda x:abs(x-0.25)))[0][0]
    value2 = np.where(normcum == min(normcum, key=lambda x:abs(x-0.75)))[0][0]
    
    denominador = np.max(image)-np.min(image)
    
    # Avoid division by zero
    if denominador == 0:
        denominador = 1
    
    hs = (value2 - value1)/denominador
    
    return hs
  
  #################################################################################
  # HAZINESS
  #################################################################################
  
def recortar_quadrado(image, size):
    """
    Pops a square (size, size) from the image.
    The square is in a random position in the image.

    Parameters
    ----------
    image : array  
        Image.
    size : int, float
        Size of the square.

    Returns
    ----------
    image : array
        A random piece of square of the original image.

    """
    # size do quadrado:
    x, y = image.shape
    
    # Interval to remove the square. Avoiding borders.
    intervalx = x - size
    intervaly = y - size

    pointx = np.random.randint(0, intervalx)
    pointy = np.random.randint(0, intervaly)

    rectangle = [pointx, pointy, pointx + size, pointy + size]
    cut = image[rectangle[0]:rectangle[2], rectangle[1]:rectangle[3]]

    return cut
  
def histo_norm(image):
    """
    Calculates the normalized histogram of an image.
    That is, the sum of all values is one. 
    The shape of the histogram is the same of the original

    Parameters
    ----------
    image : array
        Image array.

    Returns
    ----------
    hist : array
        Normalized histogram.

    """
    # pega o histograma da image, equivalente ao imhist do matlab
    # Histogram of image, similar to matlab's imhist
    count, _ = np.histogram(image, bins=256, range=[0, 256])
    histo = count / sum(count)
    
    return histo
  
def haziness_abs_norm(image, size=None):
    """
    Calculates the Haziness metric for the image.
    Cuts two squares in the image, one for the background (B) and 
    the other for the foreground (F).
    Calculates the normalized histogram for both.
    The metric is defined as the absolute value of the B histogram minus 
    F histogram, divided by their sum (B_hist + F_hist).
    That is, we normalize the metric in the range [0,1]

    Parameters
    ----------
    image : array
        Image array.
    
    size : int
        Size of the squares to be compared in the image.
        If None, default is 2.

    Returns
    ----------
    value : float
        Value of the Haziness metric for the image.
        The range is [0,1].

    """
    if size is None:
        size = 2
    
    Back = recortar_quadrado(image, size)
    Fore = recortar_quadrado(image, size)

    histoBack = histo_norm(Back)
    histoFore = histo_norm(Fore)

    z = abs(histoBack - histoFore)
    
    z = z * 255
    zsoma = histoBack + histoFore
    zsoma = zsoma * 255
    zsoma = sum(zsoma)
    if zsoma == 0:
        zsoma = 1
    return sum(z)/zsoma
  
def haziness_mean_std(image, N, size):
    """
    This function runs N squares of the size 'size' in the image.
    Returns:
        list with means, list with standard deviations
    """
    lista = []
    for _ in range(N):
        temp = haziness_abs_norm(image, size)
        lista.append(temp)
    # print('desvio padrao = ', "%.2f" % (np.std(lista)))
    return np.mean(lista), np.std(lista)
  
  
