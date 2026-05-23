exports.getUserProfile = async (req, res) => {
  try {
    const userId = req.user.userId;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          id: userId,
          name: 'Usuario Demo',
          email: 'demo@example.com',
          bio: 'Mi biografía demo',
          profileImage: 'https://via.placeholder.com/150',
          preferences: {
            language: 'es',
            theme: 'light',
          },
        },
      });
    }

    const User = require('../models/User');
    const user = await User.findById(userId).select('-password');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ data: user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateUserProfile = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { name, bio, profileImage, preferences } = req.body;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        message: 'Profile updated successfully (DEMO MODE)',
        data: {
          id: userId,
          name: name || 'Usuario Demo',
          bio: bio || '',
          profileImage: profileImage || '',
          preferences: preferences || { language: 'es', theme: 'light' },
        },
      });
    }

    const User = require('../models/User');
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    if (name) user.name = name;
    if (bio) user.bio = bio;
    if (profileImage) user.profileImage = profileImage;
    if (preferences) {
      if (preferences.language) user.preferences.language = preferences.language;
      if (preferences.theme) user.preferences.theme = preferences.theme;
    }

    await user.save();

    res.json({
      message: 'Profile updated successfully',
      data: user,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.changePassword = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
      return res.status(400).json({ error: 'Current and new passwords are required' });
    }

    if (process.env.DEMO_MODE === 'true') {
      return res.json({ message: 'Password changed successfully (DEMO MODE)' });
    }

    const User = require('../models/User');
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const isMatch = await user.comparePassword(currentPassword);
    if (!isMatch) {
      return res.status(401).json({ error: 'Current password is incorrect' });
    }

    user.password = newPassword;
    await user.save();

    res.json({ message: 'Password changed successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getPublicUserProfile = async (req, res) => {
  try {
    const { id } = req.params;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          id: id,
          name: 'Usuario Público Demo',
          bio: 'Bio pública demo',
          profileImage: 'https://via.placeholder.com/150',
        },
      });
    }

    const User = require('../models/User');
    const user = await User.findById(id).select('name bio profileImage createdAt');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ data: user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.deleteAccount = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { password } = req.body;

    if (!password) {
      return res.status(400).json({ error: 'Password required to delete account' });
    }

    if (process.env.DEMO_MODE === 'true') {
      return res.json({ message: 'Account deleted successfully (DEMO MODE)' });
    }

    const User = require('../models/User');
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Incorrect password' });
    }

    await User.deleteOne({ _id: userId });

    res.json({ message: 'Account deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
