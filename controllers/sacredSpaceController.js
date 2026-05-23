exports.getSacredSpaces = async (req, res) => {
  try {
    if (process.env.DEMO_MODE === 'true') {
      const demoSpaces = [
        {
          title: 'Santuario de Calma',
          description: 'Un espacio para la tranquilidad interior',
          ambiance: 'calm',
        },
        {
          title: 'Montaña Sagrada',
          description: 'Conexión con tu poder interior',
          ambiance: 'grounding',
        },
      ];
      return res.json({
        data: demoSpaces,
        pagination: { total: 2, page: 1, limit: 10, pages: 1 },
        message: 'Sacred spaces retrieved successfully (DEMO MODE)',
      });
    }

    const SacredSpace = require('../models/SacredSpace');
    const { page = 1, limit = 10, ambiance } = req.query;

    let query = { isActive: true };
    if (ambiance) query.ambiance = ambiance;

    const skip = (page - 1) * limit;

    const spaces = await SacredSpace.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await SacredSpace.countDocuments(query);

    res.json({
      data: spaces,
      pagination: {
        total,
        page: parseInt(page),
        limit: parseInt(limit),
        pages: Math.ceil(total / limit),
      },
      message: 'Sacred spaces retrieved successfully',
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getSacredSpace = async (req, res) => {
  try {
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          title: 'Demo Sacred Space',
          description: 'This is demo sacred space',
          ambiance: 'calm',
        },
      });
    }

    const SacredSpace = require('../models/SacredSpace');
    const { id } = req.params;

    const space = await SacredSpace.findById(id);

    if (!space) {
      return res.status(404).json({ error: 'Sacred space not found' });
    }

    res.json({ data: space });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.createSacredSpace = async (req, res) => {
  try {
    const { title, description, content, image, ambiance } = req.body;

    if (!title || !description || !content) {
      return res.status(400).json({ error: 'Title, description, and content are required' });
    }

    if (process.env.DEMO_MODE === 'true') {
      return res.status(201).json({
        message: 'Sacred space created successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const SacredSpace = require('../models/SacredSpace');
    const space = new SacredSpace({
      title,
      description,
      content,
      image: image || null,
      ambiance: ambiance || 'calm',
    });

    await space.save();

    res.status(201).json({
      message: 'Sacred space created successfully',
      data: space,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateSacredSpace = async (req, res) => {
  try {
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        message: 'Sacred space updated successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const SacredSpace = require('../models/SacredSpace');
    const { id } = req.params;
    const { title, description, content, image, ambiance, isActive } = req.body;

    const space = await SacredSpace.findById(id);

    if (!space) {
      return res.status(404).json({ error: 'Sacred space not found' });
    }

    if (title) space.title = title;
    if (description) space.description = description;
    if (content) space.content = content;
    if (image) space.image = image;
    if (ambiance) space.ambiance = ambiance;
    if (typeof isActive !== 'undefined') space.isActive = isActive;

    await space.save();

    res.json({
      message: 'Sacred space updated successfully',
      data: space,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.deleteSacredSpace = async (req, res) => {
  try {
    if (process.env.DEMO_MODE === 'true') {
      return res.json({ message: 'Sacred space deleted successfully (DEMO MODE)' });
    }

    const SacredSpace = require('../models/SacredSpace');
    const { id } = req.params;

    const space = await SacredSpace.findById(id);

    if (!space) {
      return res.status(404).json({ error: 'Sacred space not found' });
    }

    await SacredSpace.deleteOne({ _id: id });

    res.json({ message: 'Sacred space deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
