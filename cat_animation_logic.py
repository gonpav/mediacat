import random
from enum import Enum

class AnimationType(Enum):
    # idle states
    STAY = 0
    STAY_MOVE_HEAD = 1
    STAY_SHARP_CLAWS = 2
    SIT = 75
    # transitions
    SIT_DOWN = 70 # Stay => Sit
    STAND_UP = 79 # Sit => Stay
    # interactions
    STAY_CARESS = 3
    SIT_CARESS = 10 

animationPresets = {}
# animationPresets [AnimationType.KEY] = [ animation_switch.par.index, animation_range.par.torange1, animation_range.par.torange2]
animationPresets[AnimationType.STAY]                   = [0, 0, 1]
animationPresets[AnimationType.STAY_MOVE_HEAD]         = [1, 0, 1]
animationPresets[AnimationType.STAY_SHARP_CLAWS]       = [2, 0, 1]
animationPresets[AnimationType.STAY_CARESS]            = [3, 0, 1]
animationPresets[AnimationType.SIT]                    = [7, 0.15, 0.9]
animationPresets[AnimationType.SIT_DOWN]               = [7, 0, 0.15]
animationPresets[AnimationType.STAND_UP]               = [7, 0.9, 1]
animationPresets[AnimationType.SIT_CARESS]             = [10, 0, 1]

# To calculate LFO.frequency:
#   multiplier = 1/(animation_range.par.torange2 - animation_range.par.torange1)
#   lfo1.par.frequency = op('anim_length')['length']/lfo1.time.rate)*multiplier

def onAnimationDone(anim_play_count):
	#animIndex = AnimationType.STAY
	#print (animationPresets[animIndex])
	#print(anim_play_count)
	#print (op('interaction_btn').panel.state)
	
	#opAnimPlayCount = op('anim_play_count')
	#opLfo = op('lfo1')
	#print(opAnimPlayCount[0].vals)
	#print(opAnimPlayCount.pars())
	#print(opAnimPlayCount['length'])
	
	#	op('../global_vars').setVar ('gvPlayerInScene', False);
	print('Reading PlayerInScene %s' % (op('../../../global_vars').var ('gvPlayerInScene')) )

	#isInteracting = op('interaction_btn').panel.state == 1
	isInteracting = True if (op('../../../global_vars').var ('gvPlayerInScene') == 'True') else False
	print('Is interacting %s' % (isInteracting) )
	
	if isInteracting or shouldSwitchIdleAnimation(anim_play_count):
		resetOnAnimationChange(tryNextAnimation(anim_play_count, isInteracting))		
	else: 
		resetOnAnimationChange(False)
	return

def resetOnAnimationChange(should_reset):

	opAnimPlayCount = op('anim_play_count')
	opLfo = op('lfo1')

	if should_reset == True:
		opAnimPlayCount.par.reset = 0 if opAnimPlayCount.par.reset == 1 else 1	
		opLfo.par.reset = 0 if opLfo.par.reset == 1 else 1
	else: 
		opAnimPlayCount.par.reset = 0
		opLfo.par.reset = 0			
	return 

def shouldSwitchIdleAnimation(anim_play_count):
	
	shouldSwitch = False
	recommenedPlayCount = getRecommendedPlayCountForIdleAnimation(getCurrentAnimation())
			
	if anim_play_count >= recommenedPlayCount:
		shouldSwitch = True
	 
	return shouldSwitch;

def getRecommendedPlayCountForIdleAnimation(anim):
	maxPlayCount = 1
	
	if anim == AnimationType.STAY:
		maxPlayCount = 2
	elif anim == AnimationType.STAY_MOVE_HEAD:
		maxPlayCount = 2
	elif anim == AnimationType.STAY_SHARP_CLAWS:
		maxPlayCount = 1
	elif anim == AnimationType.SIT:
		maxPlayCount = 2
	elif anim == AnimationType.SIT_DOWN:
		maxPlayCount = 0
	elif anim == AnimationType.STAND_UP:
		maxPlayCount = 0
	elif anim == AnimationType.STAY_CARESS:
		maxPlayCount = 1
	elif anim == AnimationType.SIT_CARESS:
		maxPlayCount = 1
			
	return maxPlayCount


def getDefaultAnimation():
	#opAnimSwitch = op('animation_switch')
	#print ("We are here %d" % (opAnimSwitch.par.index))
	#return opAnimSwitch.par.index
	
	# We MUST make sure that op('animation_switch') contains at least 1 animation in the list of inputs
	return AnimationType.STAY


def getNextNonInteractiveAnimationCandidates(current_anim):
		
	if (current_anim == AnimationType.STAY or
	current_anim == AnimationType.STAY_MOVE_HEAD or
	current_anim == AnimationType.STAY_SHARP_CLAWS or
	current_anim == AnimationType.STAY_CARESS):
		# can stay or sit down
		return random.choice([AnimationType.STAY, AnimationType.STAY_MOVE_HEAD, AnimationType.STAY_SHARP_CLAWS]) # , AnimationType.SIT_DOWN
	
	if (current_anim == AnimationType.SIT or 
	current_anim == AnimationType.SIT_CARESS):
		# can sit or stand up
		return random.choice([AnimationType.SIT, AnimationType.STAND_UP]) 
		
	if (current_anim == AnimationType.SIT_DOWN):
		return AnimationType.SIT

	if (current_anim == AnimationType.STAND_UP):
		# can stay
		return random.choice([AnimationType.STAY, AnimationType.STAY_MOVE_HEAD, AnimationType.STAY_SHARP_CLAWS])
			
	return AnimationType.STAY

	
def getDefaultNextIdleAnimation(current_anim):
	if current_anim == AnimationType.STAY:
		return AnimationType.STAY_MOVE_HEAD
	elif current_anim == AnimationType.STAY_MOVE_HEAD:
		return AnimationType.STAY_SHARP_CLAWS
	elif current_anim == AnimationType.STAY_SHARP_CLAWS:
		return AnimationType.STAY
	elif current_anim == AnimationType.SIT:
		return AnimationType.STAND_UP
	elif current_anim == AnimationType.SIT_DOWN:
		return AnimationType.SIT
	elif current_anim == AnimationType.STAND_UP:
		return AnimationType.STAY
	elif current_anim == AnimationType.STAY_CARESS:
		return AnimationType.STAY	
	elif current_anim == AnimationType.SIT_CARESS:
		return AnimationType.SIT		
			
	return getDefaultAnimation()


def getNextInteractiveAnimation(current_anim):
	if (current_anim == AnimationType.STAY or
	current_anim == AnimationType.STAY_MOVE_HEAD or
	current_anim == AnimationType.STAY_SHARP_CLAWS or
	current_anim == AnimationType.STAY_CARESS or 
	current_anim == AnimationType.STAND_UP):
		return AnimationType.STAY_CARESS
	
	if (current_anim == AnimationType.SIT or
	current_anim == AnimationType.SIT_DOWN or
	current_anim == AnimationType.SIT_CARESS):
		return AnimationType.SIT_CARESS
		
	return getDefaultAnimation()
	
		
def getCurrentAnimation():
	currentAnim = me.fetch('currentAnim1', getDefaultAnimation()) #default value is stored in switch.index
	#print(currentAnim)  
	return currentAnim;
	

def tryNextAnimation(anim_play_count, is_interacting):	

	currentAnimation = getCurrentAnimation()
	nextAnimation = currentAnimation
	
	if is_interacting:
		nextAnimation = getNextInteractiveAnimation(currentAnimation)
	else: 
		# below code works for standing animations only
		#nextAnimationInt = random.randint(0,2)		
		nextAnimation = getNextNonInteractiveAnimationCandidates(currentAnimation)
		
		#print("Current animation %s; Next animation candidate: %s" % (currentAnimation,nextAnimation))
		
		if nextAnimation == currentAnimation:
			# if new animation is the same as current, then change it anyway 
			# if it exceeds the recommended count of plays more than 2 times 
			recommenedPlayCount = getRecommendedPlayCountForIdleAnimation(currentAnimation)
			if (recommenedPlayCount * 2) <= anim_play_count:
				print("Cat current animation %s exceeds recommendation %d more than twice" % (nextAnimation, recommenedPlayCount))
				nextAnimation = getDefaultNextIdleAnimation(currentAnimation) 
		
	# remember new animation if it actually changed		
	if nextAnimation != currentAnimation:
		setAnimation(nextAnimation)
	
	#print("Cat changed animation: %s ==> %s" % (currentAnimation ,nextAnimation))
	
	return currentAnimation != nextAnimation


def setAnimation(anim):

	animationFileLength = op('anim_length')['length']
        
	# change animation file	
	opAnimSwitch = op('animation_switch')
	opAnimSwitch.par.index = animationPresets[anim][0]
	
	# change animation range
	opAnimationRange = op('animation_range')
	#opAnimationRange.par.torange1 = animationPresets[anim][1]
	#opAnimationRange.par.torange2 = animationPresets[anim][2]

	#print("Current amim length2: %f" % op('anim_length2').par.value0)
	#op('anim_length2').par.value0 = animationFileLength - animationFileLength * (animationPresets[anim][2] - animationPresets[anim][1])
	#print("Current amim length2: %f" % op('anim_length2').par.value0)

    # update current_frame range
	opCurrentFrame = op('current_frame')
	#print("Current_frame: %f" % opCurrentFrame.par.torange2)
	#opCurrentFrame.par.torange2 = op('anim_length2').par.value0
	#print("New current_frame: %f" % opCurrentFrame.par.torange2)
        
	# Re-calculate LFO.frequency:
	#   multiplier = 1/(animation_range.par.torange2 - animation_range.par.torange1)
	#   lfo1.par.frequency = op('anim_length')['length']/lfo1.time.rate)*multiplier
	opLfo = op('lfo1')
	#print("Current LFO frequency: %f" % opLfo.par.frequency)
	
	multiplier = 1/(animationPresets[anim][2] - animationPresets[anim][1])
	#print("multiplier: %f" % multiplier)
	
	#opLfo.par.frequency = 1/(animationFileLength/opLfo.time.rate)*multiplier
	#print("newFrequency: %f" % opLfo.par.frequency)
	
	# save current animation
	me.store('currentAnim1', anim)
	return
