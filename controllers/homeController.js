// Obtener datos del Home/Hero
exports.getHome = async (req, res) => {
  try {
    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        data: {
          title: 'Manifestation Journal',
          subtitle: 'Tu espacio para rituales, intenciones y crecimiento personal',
          description: 'Un diario sagrado donde tus intenciones cobran vida. Registra rituales, manifestaciones y observa tu crecimiento energético.',
          tagline: 'Manifiesta tu realidad, cultiva tu energía',
          isActive: true,
        },
        message: 'Home data retrieved successfully (DEMO MODE)',
      });
    }

    const Home = require('../models/Home');
    let home = await Home.findOne();

    if (!home) {
      home = new Home();
      await home.save();
    }

    res.json({
      data: home,
      message: 'Home data retrieved successfully',
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Actualizar datos del Home (Admin)
exports.updateHome = async (req, res) => {
  try {
    // DEMO MODE
    if (process.env.DEMO_MODE === 'true') {
      return res.json({
        message: 'Home updated successfully (DEMO MODE)',
        data: req.body,
      });
    }

    const Home = require('../models/Home');
    const { title, subtitle, description, heroImage, tagline } = req.body;

    let home = await Home.findOne();

    if (!home) {
      home = new Home();
    }

    if (title) home.title = title;
    if (subtitle) home.subtitle = subtitle;
    if (description) home.description = description;
    if (heroImage) home.heroImage = heroImage;
    if (tagline) home.tagline = tagline;

    await home.save();

    res.json({
      message: 'Home updated successfully',
      data: home,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
