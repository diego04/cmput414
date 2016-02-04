from pyfbsdk import *

#this is the stuff you gave us
def skew_sym(v):
    '''
    Returns skew-symetric matrix for vector v
    '''
    m = FBMatrix([
    0, -v[2], v[1], 0,
    v[2], 0, -v[0], 0,
    -v[1], v[0], 0, 0,
    0, 0, 0, 1
    ])
    # IMPORTANT!: In MoBu, matrices are row-major, need to transpose it
    m.Transpose()
    return m
    
#this is the stuff you gave us
def align_matrix(a,b):
    '''
    Returns matrix that rotates vector a onto vector b
    '''
    a.Normalize()
    b.Normalize()
    
    
    v = a.CrossProduct(b)
    s = v.Length() # Sin of angle
    c = a.DotProduct(b) # Cos of angle
    
    # Load identity
    I = FBMatrix()
 
    # a is prallel to b ( return identity)
    if v.Length() == 0:
        return I
        
    
    skew_M = skew_sym(v)
    
    R = I +  skew_M + (skew_M*skew_M)*((1-c)/(s*s))
    R[15] = 1 # Can' use 3x3 here
    return R
    
#find the number of bones as a multipler for iterations
def getBoneCount(root):
    count = 0
    while root.Children:
        root = root.Children[0]
        count += 1
    return count

#get the last node
def getLeaf(root):
    while root.Children:
        root = root.Children[0]
    return root
    
#get vector form of node
def getVector(marker):
    m_pos = FBVector3d()
    marker.GetVector(m_pos,FBModelTransformationType.kModelTranslation)
    return m_pos


#this is our assignment to hand in
#i hope the variable names are self documenting
#i feel my code is simple enough to understand that it does not need commenting
#it is pretty much the algorithm you gave in class
def ccd(goal,chain_base):
    
    deviation = 0.01
    iterations = 0
    iterationBound = getBoneCount(chain_base) * 10
    
    leaf = getLeaf(chain_base)
    effector = leaf

    leafVector = getVector(leaf)
    goalVector = getVector(goal)
    
    distance = goalVector-leafVector
    goalDistance = distance.Length()

    while ((iterationBound>iterations) and (goalDistance>deviation)):
        FBSystem().Scene.Evaluate()
        
        leafVector = getVector(leaf)
        goalVector = getVector(goal)
    
        effectorVector = FBVector3d()
        effector.Parent.GetVector(effectorVector,FBModelTransformationType.kModelTranslation)
        
        vectorBuildA = leafVector - effectorVector
        vectorBuildB = goalVector- effectorVector
        
        targetMatrix = align_matrix(vectorBuildA,vectorBuildB)
        
        cur_Ori = FBMatrix()
        effector.Parent.GetMatrix(cur_Ori,FBModelTransformationType.kModelRotation,False)

        final_Ori = targetMatrix * cur_Ori
        ori_vec = FBVector3d()
        FBMatrixToRotation(ori_vec,final_Ori)
        effector.Parent.Rotation = ori_vec
       
        if effector.Parent==chain_base:
            effector = leaf
        else:
            effector = effector.Parent
   
        
        goalDistance = goalVector-leafVector
        goalDistance = goalDistance.Length()
        iterations=iterations+1
 
# Test
#goal = FBFindModelByLabelName('Goal')
#chain_base = FBFindModelByLabelName('Node')
#ccd(goal,chain_base)
