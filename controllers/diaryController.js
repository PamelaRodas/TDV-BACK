exports.getEntries = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { page = 1, limit = 10, type, energy } = req.query;

    if (process.env.DEMO_MODE === 'true') {
      const demoEntries = [
        {
          title: 'Mi Manifestación de Hoy',
          content: 'He manifestado abundancia y paz interior.',
          type: 'manifestation',
          energy: 'high',
          tags: ['abundancia', 'paz'],
          isPublic: false,
        },
        {
          title: 'Ritual Sagrado',
          content: 'Completé mi ritual de la mañana con intención.',
          type: 'ritual',
          energy: 'medium',
          tags: ['ritual', 'mañana'],
          isPublic: false,
        },
      ];
      return res.json({
        data: demoEntries,
        pagination: {
          total: 2,
          page: 1,
          limit: 10,
          pages: 1,
        },
        message: 'Entries retrieved successfully (DEMO MODE)',
      });
    }

    let query = { userId };

    if (type) query.type = type;
    if (energy) query.energy = energy;

    const skip = (page - 1) * limit;

    const Entry = require('../models/Entry');
    const entries = await Entry.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Entry.countDocuments(query);

    res.json({
      data: entries,
      pagination: {
        total,
        page: parseInt(page),
        limit: parseInt(limit),
        pages: Math.ceil(total / limit),
      },
      message: 'Entries retrieved successfully',
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getEntry = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          title: 'Demo Entry',
          content: 'This is a demo diary entry.',
          type: 'manifestation',
          energy: 'medium',
        },
      });
    }

    const Entry = require('../models/Entry');
    const entry = await Entry.findById(id);

    if (!entry) {
      return res.status(404).json({ error: 'Entry not found' });
    }

    if (entry.userId.toString() !== userId && !entry.isPublic) {
      return res.status(403).json({ error: 'Access denied' });
    }

    res.json({ data: entry });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.createEntry = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { title, content, type, energy, tags, images, isPublic } = req.body;

    if (!title || !content) {
      return res.status(400).json({ error: 'Title and content are required' });
    }

    if (process.env.DEMO_MODE === 'true') {
      return res.status(201).json({
        message: 'Entry created successfully (DEMO MODE)',
        data: {
          userId,
          title,
          content,
          type: type || 'manifestation',
          energy: energy || 'medium',
          tags: tags || [],
          images: images || [],
          isPublic: isPublic || false,
        },
      });
    }

    const Entry = require('../models/Entry');
    const entry = new Entry({
      userId,
      title,
      content,
      type: type || 'manifestation',
      energy: energy || 'medium',
      tags: tags || [],
      images: images || [],
      isPublic: isPublic || false,
    });

    await entry.save();

    res.status(201).json({
      message: 'Entry created successfully',
      data: entry,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateEntry = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;
    const { title, content, type, energy, tags, images, isPublic } = req.body;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        message: 'Entry updated successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const Entry = require('../models/Entry');
    const entry = await Entry.findById(id);

    if (!entry) {
      return res.status(404).json({ error: 'Entry not found' });
    }

    if (entry.userId.toString() !== userId) {
      return res.status(403).json({ error: 'Access denied' });
    }

    if (title) entry.title = title;
    if (content) entry.content = content;
    if (type) entry.type = type;
    if (energy) entry.energy = energy;
    if (tags) entry.tags = tags;
    if (images) entry.images = images;
    if (typeof isPublic !== 'undefined') entry.isPublic = isPublic;

    await entry.save();

    res.json({
      message: 'Entry updated successfully',
      data: entry,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.deleteEntry = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({ message: 'Entry deleted successfully (DEMO MODE)' });
    }

    const Entry = require('../models/Entry');
    const entry = await Entry.findById(id);

    if (!entry) {
      return res.status(404).json({ error: 'Entry not found' });
    }

    if (entry.userId.toString() !== userId) {
      return res.status(403).json({ error: 'Access denied' });
    }

    await Entry.deleteOne({ _id: id });

    res.json({ message: 'Entry deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getDiaryStats = async (req, res) => {
  try {
    const userId = req.user.userId;

    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          totalEntries: 15,
          typeBreakdown: [
            { _id: 'manifestation', count: 7 },
            { _id: 'ritual', count: 5 },
            { _id: 'reflection', count: 3 },
          ],
          energyBreakdown: [
            { _id: 'high', count: 6 },
            { _id: 'medium', count: 7 },
            { _id: 'low', count: 2 },
          ],
        },
        message: 'Diary statistics retrieved successfully (DEMO MODE)',
      });
    }

    const Entry = require('../models/Entry');
    const totalEntries = await Entry.countDocuments({ userId });
    const typeBreakdown = await Entry.aggregate([
      { $match: { userId: require('mongoose').Types.ObjectId(userId) } },
      { $group: { _id: '$type', count: { $sum: 1 } } },
    ]);

    const energyBreakdown = await Entry.aggregate([
      { $match: { userId: require('mongoose').Types.ObjectId(userId) } },
      { $group: { _id: '$energy', count: { $sum: 1 } } },
    ]);

    res.json({
      data: {
        totalEntries,
        typeBreakdown,
        energyBreakdown,
      },
      message: 'Diary statistics retrieved successfully',
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
