// Obtener todas las fotos del usuario
exports.getPhotos = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { page = 1, limit = 12, energy } = req.query;

    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      const demoPhotos = [
        {
          url: 'https://via.placeholder.com/300x300?text=Photo+1',
          title: 'Mi Foto 1',
          description: 'Una foto hermosa',
          energy: 'high',
          tags: ['naturaleza'],
        },
        {
          url: 'https://via.placeholder.com/300x300?text=Photo+2',
          title: 'Mi Foto 2',
          description: 'Otro recuerdo',
          energy: 'medium',
          tags: ['viaje'],
        },
      ];
      return res.json({
        data: demoPhotos,
        pagination: {
          total: 2,
          page: 1,
          limit: 12,
          pages: 1,
        },
        message: 'Photos retrieved successfully (DEMO MODE)',
      });
    }

    let query = { userId };
    if (energy) query.energy = energy;

    const skip = (page - 1) * limit;

    const Photo = require('../models/Photo');
    const photos = await Photo.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Photo.countDocuments(query);

    res.json({
      data: photos,
      pagination: {
        total,
        page: parseInt(page),
        limit: parseInt(limit),
        pages: Math.ceil(total / limit),
      },
      message: 'Photos retrieved successfully',
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Obtener una foto específica
exports.getPhoto = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          url: 'https://via.placeholder.com/300x300?text=Demo+Photo',
          title: 'Demo Photo',
          description: 'This is a demo photo',
          energy: 'medium',
        },
      });
    }

    const Photo = require('../models/Photo');
    const photo = await Photo.findById(id);

    if (!photo) {
      return res.status(404).json({ error: 'Photo not found' });
    }

    if (photo.userId.toString() !== userId && !photo.isPublic) {
      return res.status(403).json({ error: 'Access denied' });
    }

    res.json({ data: photo });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Crear nueva foto
exports.createPhoto = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { url, title, description, caption, tags, energy, isPublic } = req.body;

    if (!url) {
      return res.status(400).json({ error: 'URL is required' });
    }

    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.status(201).json({
        message: 'Photo created successfully (DEMO MODE)',
        data: {
          userId,
          url,
          title: title || '',
          description: description || '',
          caption: caption || '',
          tags: tags || [],
          energy: energy || 'medium',
          isPublic: isPublic || false,
        },
      });
    }

    const Photo = require('../models/Photo');
    const photo = new Photo({
      userId,
      url,
      title: title || '',
      description: description || '',
      caption: caption || '',
      tags: tags || [],
      energy: energy || 'medium',
      isPublic: isPublic || false,
    });

    await photo.save();

    res.status(201).json({
      message: 'Photo created successfully',
      data: photo,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Actualizar foto
exports.updatePhoto = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;
    const { title, description, caption, tags, energy, isPublic } = req.body;

    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        message: 'Photo updated successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const Photo = require('../models/Photo');
    const photo = await Photo.findById(id);

    if (!photo) {
      return res.status(404).json({ error: 'Photo not found' });
    }

    if (photo.userId.toString() !== userId) {
      return res.status(403).json({ error: 'Access denied' });
    }

    if (title) photo.title = title;
    if (description) photo.description = description;
    if (caption) photo.caption = caption;
    if (tags) photo.tags = tags;
    if (energy) photo.energy = energy;
    if (typeof isPublic !== 'undefined') photo.isPublic = isPublic;

    await photo.save();

    res.json({
      message: 'Photo updated successfully',
      data: photo,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Eliminar foto
exports.deletePhoto = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({ message: 'Photo deleted successfully (DEMO MODE)' });
    }

    const Photo = require('../models/Photo');
    const photo = await Photo.findById(id);

    if (!photo) {
      return res.status(404).json({ error: 'Photo not found' });
    }

    if (photo.userId.toString() !== userId) {
      return res.status(403).json({ error: 'Access denied' });
    }

    await Photo.deleteOne({ _id: id });

    res.json({ message: 'Photo deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
