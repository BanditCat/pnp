import numpy as np

#http://web.cecs.pdx.edu/~whung/papers/ASPDAC-2005-reverse.pdf



# A permutation is just a numpy array of the permuted indices. e.g. [ 1, 0, 3, 2 ] is a not gate on bit 0.
# A gate set is just a sorted, uniqueified 2d array of permutations

# gates
def notGate( bits, bit ):
    return np.array( [ i ^ ( 2 ** bit ) for i in range( 2 ** bits ) ], dtype = np.uint32 )
def feynman( bits, bit, control ):
    return np.array( [ i ^ ( 2 ** bit )
                       if i & ( 2 ** control )
                       else i
                       for i in range( 2 ** bits ) ], dtype = np.uint32 ) 
def toffoli( bits, bit, control1, control2 ):
    return np.array( [ i ^ ( 2 ** bit )
                       if i & ( 2 ** control1 ) and i & ( 2 ** control2 )
                       else i
                       for i in range( 2 ** bits ) ], dtype = np.uint32 ) 


# NOT, Feynman, Toffoli gate library
def NFT( bits ):
    ans = []
    for i in range( bits ):
        ans.append( notGate( bits, i ) )
        for j in range( bits ):
            if j != i:
                ans.append( feynman( bits, i, j ) )
                for k in range( bits ):
                    if j != i and j != k and k != i:
                        ans.append( toffoli( bits, i, j, k ) )
    return np.unique( np.array( ans ), axis = 0 )

# cheese as in cheesy
# returns the product of two gate sets. Does not unique.
def cheeseProduct( setA, setB ):
    ans = np.empty( ( len( setA ) * len( setB ), len( setA[ 0 ] ) ), dtype = np.uint32 )
    ind = 0
    for i in range( len( setA ) ):
        for j in range( len( setB ) ):
            ans[ ind ] = setA[ i ][ setB[ j ] ]
            ind += 1
    return ans

# set difference on two gate sets.
def setdiff2d( a, b ):
    nr, nc = a.shape
    dtype = { 'names' : [ 'f{}'.format( i ) for i in range( nc ) ],
              'formats' : nc * [ a.dtype ] }
    ans = np.setdiff1d( a.view( dtype ), b.view( dtype ) )
    ans = ans.view( a.dtype ).reshape( -1, nc )
    return ans
     

def FML( lib ):
    null = np.arange( 0, len( lib[ 0 ] ), dtype = np.uint32 ).reshape( 1, -1 )
    gatesThatTakeNOrUnderN = [ null ]
    gatesThatTakeN = [ null ]
    lastsize = 1
    while lastsize != 0:
        last = gatesThatTakeNOrUnderN[ len( gatesThatTakeNOrUnderN ) - 1 ]
        next = np.append( last, cheeseProduct( last, lib ), axis = 0 )
        next = np.unique( next, axis = 0 )
        nextgttn = setdiff2d( next, last )
        gatesThatTakeNOrUnderN.append( next )
        gatesThatTakeN.append( nextgttn )
        lastsize = len( nextgttn )
        print( lastsize )

    return( gatesThatTakeNOrUnderN[ len( gatesThatTakeNOrUnderN ) - 1 ], gatesThatTakeN )


l = NFT( 3 )
a, q = FML( l )
print( len( a ) / ( 8 * 7 * 6 * 5 * 4 * 3 * 2 ) )
