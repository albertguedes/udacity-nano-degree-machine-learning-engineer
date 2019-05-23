# TODO: your agent here!
import numpy as np
from task import Task

import random
from collections import deque, namedtuple

import tensorflow as tf
from tensorflow.contrself.ib.keras import layers, models, optimizers
from tensorflow.contrib.keras import backend as K
from tensorflow.contrib.keras import activations
from tensorflow.contrib.keras import regularizers
from tensorflow.contrib.keras import initializers

class Agent():
    def __init__(self, task):
        # Task (environment) information
        self.task = task
        self.state_size = task.state_size
        self.action_size = task.action_size
        self.action_low = task.action_low
        self.action_high = task.action_high
        self.action_range = self.action_high - self.action_low

        self.w = np.random.normal(
            size=(self.state_size, self.action_size),  # weights for simple linear policy: state_space x action_space
            scale=(self.action_range / (2 * self.state_size))) # start producing actions in a decent range

        # Score tracker and learning parameters
        self.best_w = None
        self.best_score = -np.inf
        self.noise_scale = 0.1

        # Episode variables
        self.reset_episode()

    def reset_episode(self):
        self.total_reward = 0.0
        self.count = 0
        state = self.task.reset()
        return state

    def step(self, reward, done):
        # Save experience / reward
        self.total_reward += reward
        self.count += 1

        # Learn, if at end of episode
        if done:
            self.learn()

    def act(self, state):
        # Choose action based on given state and policy
        action = np.dot(state, self.w)  # simple linear policy
        return action

    def learn(self):
        # Learn by random policy search, using a reward-based score
        self.score = self.total_reward / float(self.count) if self.count else 0.0
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_w = self.w
            self.noise_scale = max(0.5 * self.noise_scale, 0.01)
        else:
            self.w = self.best_w
            self.noise_scale = min(2.0 * self.noise_scale, 3.2)
        self.w = self.w + self.noise_scale * np.random.normal(size=self.w.shape)  # equal noise in all directions

    #
    # Train the agent.
    #
    def train(self,number_episodes, runtime=5.0, init_pos=None, target_position=None, printOut=True):

        noise_annealing = 0.001
        noise_min_sigma = 0.01

        # Handle each episode w/ state
        for i_episode in range(1, number_episodes+1):

            state = self.reset_episode()
            noise.reset(noise_annealing, noise_min_sigma)

            steps = 0
            score = 0.

            while True:
                action = self.act(state)
                action += noise.sample()
                action = np.clip(action, -1, 1)

                next_state, reward, done = self.task.step(action)
                self.step(action, reward, next_state, done)

                state = next_state
                score += reward
                steps += 1
                if done:
                    break

            avg_reward.append(score/max(1, steps))
            scores.append(score)

            if score > best_score:
                best_score = score

            if(printOut):
                text = "\r"
                text += "Episodes: {:4d}, ".format(len(scores))
                text += "Score: {:.1f}, ".format(score)
                text += "Average Score: {:.1f}, ".format(np.mean(scores[-25:]))
                text += "Best Score: {:.1f}, ".format(best_score)
                text += "Average Reward: {:.1f}, ".format(avg_reward[-1])
                text += "  "
                print(text, end="")
                sys.stdout.flush()

        return scores, grades, avg_reward, best_score, noise

class Actor:

    def __init__(self, state_size, action_size, action_low, action_high):
        self.state_size = state_size
        self.action_size = action_size
        self.action_low = action_low
        self.action_high = action_high
        self.action_range = self.action_high - self.action_low

        # Initialize any other variables here

        self.build_model()

    def build_model(self):
        l2_regularization_kernel = 1e-5

        # Input Layer
        input = layers.Input(shape=(self.state_size,), name='input_states')

        # Hidden Layers
        model = layers.Dense(units=300, kernel_regularizer=regularizers.l2(l2_regularization_kernel))(input)
        model = layers.BatchNormalization()(model)
        model = layers.LeakyReLU(1e-2)(model)

        model = layers.Dense(units=400, kernel_regularizer=regularizers.l2(l2_regularization_kernel))(model)
        model = layers.BatchNormalization()(model)
        model = layers.LeakyReLU(1e-2)(model)

        model = layers.Dense(units=200, kernel_regularizer=regularizers.l2(l2_regularization_kernel))(model)
        model = layers.BatchNormalization()(model)
        model = layers.LeakyReLU(1e-2)(model)

        # Our output layer - a fully connected layer
        output = layers.Dense(units=self.action_size, activation='tanh', kernel_regularizer=regularizers.l2(l2_regularization_kernel), kernel_initializer=initializers.RandomUniform(minval=-3e-3, maxval=3e-3), name='output_actions')(model)

        # Keras model
        self.model = models.Model(inputs=input, outputs=output)

        # Define loss and optimizer
        action_gradients = layers.Input(shape=(self.action_size,))
        loss = K.mean(-action_gradients * output)
        optimizer = optimizers.Adam(lr=1e-4)

        update_operation = optimizer.get_updates( params=self.model.trainable_weights, loss=loss)
        self.train_fn = K.function( inputs=[ self.model.input, action_gradients, K.learning_phase()],
                                    outputs=[],
                                    updates=update_operation )

class Critic:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.build_model()

    def build_model(self):
        l2_kernel_regularization = 1e-5

        # Define input layers
        input_states = layers.Input(shape=(self.state_size,), name='input_states')
        input_actions = layers.Input(shape=(self.action_size,), name='input_actions')

        # Hidden layers for states
        model_states = layers.Dense(units=300, kernel_regularizer=regularizers.l2(l2_kernel_regularization))(input_states)
        model_states = layers.BatchNormalization()(model_states)
        model_states = layers.LeakyReLU(1e-2)(model_states)

        model_states = layers.Dense(units=400, kernel_regularizer=regularizers.l2(l2_kernel_regularization))(model_states)
        model_states = layers.BatchNormalization()(model_states)
        model_states = layers.LeakyReLU(1e-2)(model_states)

        # Hidden layers for actions
        model_actions = layers.Dense(units=400, kernel_regularizer=regularizers.l2(l2_kernel_regularization))(input_actions)
        model_actions = layers.BatchNormalization()(model_actions)
        model_actions = layers.LeakyReLU(1e-2)(model_actions)

        # Both models merge here
        model = layers.add([model_states, model_actions])

        # Fully connected and batch normalization
        model = layers.Dense(units=200, kernel_regularizer=regularizers.l2(l2_kernel_regularization))(model)
        model = layers.BatchNormalization()(model)
        model = layers.LeakyReLU(1e-2)(model)

        # Q values / output layer
        Q_values = layers.Dense(units=1, activation=None, kernel_regularizer=regularizers.l2(l2_kernel_regularization),
                                kernel_initializer=initializers.RandomUniform(minval=-5e-3, maxval=5e-3),
                                name='output_Q_values')(model)

        # Keras wrap the model
        self.model = models.Model(inputs=[input_states, input_actions], outputs=Q_values)
        optimizer = optimizers.Adam(lr=1e-2)
        self.model.compile(optimizer=optimizer, loss='mse')
        action_gradients = K.gradients(Q_values, input_actions)
        self.get_action_gradients = K.function(inputs=[*self.model.input, K.learning_phase()], outputs=action_gradients)

class DDPG():
    """Reinforcement Learning agent that learns using DDPG."""
    def __init__(self, task):
        self.task = task
        self.state_size = task.state_size
        self.action_size = task.action_size
        self.action_low = task.action_low
        self.action_high = task.action_high

        # Actor (Policy) Model
        self.actor_local = Actor(self.state_size, self.action_size, self.action_low, self.action_high)
        self.actor_target = Actor(self.state_size, self.action_size, self.action_low, self.action_high)

        # Critic (Value) Model
        self.critic_local = Critic(self.state_size, self.action_size)
        self.critic_target = Critic(self.state_size, self.action_size)

        # Initialize target model parameters with local model parameters
        self.critic_target.model.set_weights(self.critic_local.model.get_weights())
        self.actor_target.model.set_weights(self.actor_local.model.get_weights())

        # Noise process
        self.exploration_mu = 0
        self.exploration_theta = 0.15
        self.exploration_sigma = 0.2
        self.noise = OUNoise(self.action_size, self.exploration_mu, self.exploration_theta, self.exploration_sigma)

        # Replay memory
        self.buffer_size = 100000
        self.batch_size = 64
        self.memory = ReplayBuffer(self.buffer_size, self.batch_size)

        # Algorithm parameters
        self.gamma = 0.99  # discount factor
        self.tau = 0.01  # for soft update of target parameters

    def reset_episode(self):
        self.noise.reset()
        state = self.task.reset()
        self.last_state = state
        return state

    def step(self, action, reward, next_state, done):
         # Save experience / reward
        self.memory.add(self.last_state, action, reward, next_state, done)

        # Learn, if enough samples are available in memory
        if len(self.memory) > self.batch_size:
            experiences = self.memory.sample()
            self.learn(experiences)

        # Roll over last state and action
        self.last_state = next_state

    def act(self, state):
        """Returns actions for given state(s) as per current policy."""
        state = np.reshape(state, [-1, self.state_size])
        action = self.actor_local.model.predict(state)[0]
        return list(action + self.noise.sample())  # add some noise for exploration

    def learn(self, experiences):
        """Update policy and value parameters using given batch of experience tuples."""
        # Convert experience tuples to separate arrays for each element (states, actions, rewards, etc.)
        states = np.vstack([e.state for e in experiences if e is not None])
        actions = np.array([e.action for e in experiences if e is not None]).astype(np.float32).reshape(-1, self.action_size)
        rewards = np.array([e.reward for e in experiences if e is not None]).astype(np.float32).reshape(-1, 1)
        dones = np.array([e.done for e in experiences if e is not None]).astype(np.uint8).reshape(-1, 1)
        next_states = np.vstack([e.next_state for e in experiences if e is not None])

        # Get predicted next-state actions and Q values from target models
        #     Q_targets_next = critic_target(next_state, actor_target(next_state))
        actions_next = self.actor_target.model.predict_on_batch(next_states)
        Q_targets_next = self.critic_target.model.predict_on_batch([next_states, actions_next])

        # Compute Q targets for current states and train critic model (local)
        Q_targets = rewards + self.gamma * Q_targets_next * (1 - dones)
        self.critic_local.model.train_on_batch(x=[states, actions], y=Q_targets)

        # Train actor model (local)
        action_gradients = np.reshape(self.critic_local.get_action_gradients([states, actions, 0]), (-1, self.action_size))
        self.actor_local.train_fn([states, action_gradients, 1])  # custom training function

        # Soft-update target models
        self.soft_update(self.critic_local.model, self.critic_target.model)
        self.soft_update(self.actor_local.model, self.actor_target.model)

    def soft_update(self, local_model, target_model):
        """Soft update model parameters."""
        local_weights = np.array(local_model.get_weights())
        target_weights = np.array(target_model.get_weights())

        assert len(local_weights) == len(target_weights), "Local and target model parameters must have the same size"

        new_weights = self.tau * local_weights + (1 - self.tau) * target_weights
        target_model.set_weights(new_weights)

class OUNoise:
    """Ornstein-Uhlenbeck process."""

    def __init__(self, size, mu, theta, sigma):
        """Initialize parameters and noise process."""
        self.size = size
        self.mu = mu * np.ones(self.size)
        self.state = np.copy(self.mu)
        self.theta = theta
        self.sigma = sigma
        self.reset()

    def reset(self, decay=None, sigma_min=None):
        """Reset the internal state (= noise) to mean (mu)."""

        if decay is not None and sigma_min is not None:
            self.sigma = max((1-decay) * self.sigma, sigma_min)

        self.state = np.copy(self.mu)

    def sample(self):
        """Update internal state and return it as a noise sample."""
        x = self.state
        dx = self.theta * (self.mu - x) + self.sigma * np.random.randn(self.size)
        self.state = x + dx
        return self.state

    def __call__(self):
        return self.sample()

    def update_mu(self, target):
        self.mu = target

class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, buffer_size, batch_size):
        """Initialize a ReplayBuffer object.
        Params
        ======
            buffer_size: maximum size of buffer
            batch_size: size of each training batch
        """
        self.memory = deque(maxlen=buffer_size)  # internal memory (deque)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])

    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self, batch_size=64):
        """Randomly sample a batch of experiences from memory."""
        return random.sample(self.memory, k=self.batch_size)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)

class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, buffer_size, batch_size):
        """Initialize a ReplayBuffer object.
        Params
        ======
            buffer_size: maximum size of buffer
            batch_size: size of each training batch
        """
        self.memory = deque(maxlen=buffer_size)  # internal memory (deque)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])

    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self, batch_size=64):
        """Randomly sample a batch of experiences from memory."""
        return random.sample(self.memory, k=self.batch_size)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)
