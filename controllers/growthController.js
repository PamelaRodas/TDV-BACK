// Obtener todos los contenidos de Growth
exports.getGrowthContent = async (req, res) => {
  try {
    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      const demoContent = [
        {
          title: 'Meditación Matutina',
          description: 'Comienza tu día con claridad y propósito',
          category: 'meditation',
          difficulty: 'beginner',
          duration: 10,
        },
        {
          title: 'Ritual de Abundancia',
          description: 'Atraer prosperidad a tu vida',
          category: 'ritual',
          difficulty: 'beginner',
          duration: 15,
        },
      ];
      return res.json({
        data: demoContent,
        pagination: { total: 2, page: 1, limit: 10, pages: 1 },
        message: 'Growth content retrieved successfully (DEMO MODE)',
      });
    }

    const Content = require('../models/Content');
    const { page = 1, limit = 10, category, difficulty } = req.query;

    let query = { isActive: true };
    if (category) query.category = category;
    if (difficulty) query.difficulty = difficulty;

    const skip = (page - 1) * limit;

    const content = await Content.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Content.countDocuments(query);

    res.json({
      data: content,
      pagination: {
        total,
        page: parseInt(page),
        limit: parseInt(limit),
        pages: Math.ceil(total / limit),
      },
      message: 'Growth content retrieved successfully',
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Obtener un contenido específico
exports.getGrowthItem = async (req, res) => {
  try {
    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          title: 'Demo Content',
          description: 'This is demo content',
          category: 'meditation',
        },
      });
    }

    const Content = require('../models/Content');
    const { id } = req.params;

    const content = await Content.findById(id);

    if (!content) {
      return res.status(404).json({ error: 'Content not found' });
    }

    res.json({ data: content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Crear nuevo contenido (Admin)
exports.createGrowthContent = async (req, res) => {
  try {
    const { title, description, category, content, image, author, difficulty, duration } = req.body;

    if (!title || !description || !content) {
      return res.status(400).json({ error: 'Title, description, and content are required' });
    }

    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.status(201).json({
        message: 'Growth content created successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const Content = require('../models/Content');
    const newContent = new Content({
      title,
      description,
      category: category || 'practice',
      content,
      image: image || null,
      author: author || 'Manifestation Journal',
      difficulty: difficulty || 'beginner',
      duration: duration || 10,
    });

    await newContent.save();

    res.status(201).json({
      message: 'Growth content created successfully',
      data: newContent,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Actualizar contenido (Admin)
exports.updateGrowthContent = async (req, res) => {
  try {
    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        message: 'Growth content updated successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const Content = require('../models/Content');
    const { id } = req.params;
    const { title, description, category, content, image, author, difficulty, duration, isActive } = req.body;

    const growthContent = await Content.findById(id);

    if (!growthContent) {
      return res.status(404).json({ error: 'Content not found' });
    }

    if (title) growthContent.title = title;
    if (description) growthContent.description = description;
    if (category) growthContent.category = category;
    if (content) growthContent.content = content;
    if (image) growthContent.image = image;
    if (author) growthContent.author = author;
    if (difficulty) growthContent.difficulty = difficulty;
    if (duration) growthContent.duration = duration;
    if (typeof isActive !== 'undefined') growthContent.isActive = isActive;

    await growthContent.save();

    res.json({
      message: 'Growth content updated successfully',
      data: growthContent,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Eliminar contenido (Admin)
exports.deleteGrowthContent = async (req, res) => {
  try {
    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({ message: 'Growth content deleted successfully (DEMO MODE)' });
    }

    const Content = require('../models/Content');
    const { id } = req.params;

    const growthContent = await Content.findById(id);

    if (!growthContent) {
      return res.status(404).json({ error: 'Content not found' });
    }

    await Content.deleteOne({ _id: id });

    res.json({ message: 'Growth content deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
