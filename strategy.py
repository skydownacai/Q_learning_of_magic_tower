import pandas as pd
class Strategy:

	def __init__(self):
		pass

	def choose_action(self,state):
		''' recieve a state then choose_a_action ,
			the reward of this action will be a param of  Strategy.actionreward
			:return (obj,action)

		'''
		pass

	def actionreward(self,reward):

		''' recieve a reward then you can decided how to handle the reward here'''

		pass


class QLearning(Strategy):

	def __init__(self):
		self.Qtable = pd.DataFrame(
			{"state":[]}
		)
		self.Qtable = self.Qtable.set_index("state",drop=True)
		self.reset_index = False
		self.last_state = None
		self.last_action = None

	def choose_action(self,state,state_encoded):
		for item in state:
			for action in item.interact_actions:
				if action.name  not in self.Qtable:
					self.Qtable[action.name] = 0

		if state_encoded not in self.Qtable.index:
			self.Qtable = self.Qtable.append(
				{'state':state_encoded},ignore_index=True)

		if not self.reset_index:
			self.Qtable = self.Qtable.set_index("state")
			self.reset_index = True

		return (state[0],state[0].interact_actions[0])

	def actionreward(self,state):

		''' recieve a reward then you can decided how to handle the reward here'''

		pass