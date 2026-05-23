const demoModeHandler = (err, req, res, next) => {
  if (process.env.DEMO_MODE !== 'true') {
  }

  if (err.message && err.message.includes('buffering timed out')) {
    console.warn('⚠️ Database timeout - returning demo data');

    if (req.path.includes('/home')) {
      return res.json({
        data: {
          title: 'Manifestation Journal',
          subtitle: 'Tu espacio para rituales, intenciones y crecimiento personal',
          description: 'Un diario sagrado donde tus intenciones cobran vida...',
          tagline: 'Manifiesta tu realidad, cultiva tu energía',
          demo: true,
        },
      });
    }

    if (req.path.includes('/diary')) {
      return res.json({
        data: [
          {
            _id: 'demo-1',
            title: 'Mi primera manifestación',
            content: 'Hoy me propongo atraer abundancia...',
            type: 'manifestation',
            energy: 'high',
            createdAt: new Date(),
            demo: true,
          },
        ],
        pagination: { total: 1, page: 1, limit: 10, pages: 1 },
        message: 'Entries retrieved (DEMO MODE)',
      });
    }

    if (req.path.includes('/photos')) {
      return res.json({
        data: [],
        pagination: { total: 0, page: 1, limit: 12, pages: 0 },
        message: 'Photos (DEMO MODE - empty)',
      });
    }

    if (req.path.includes('/growth')) {
      return res.json({
        data: [
          {
            title: 'Meditación Matutina',
            description: 'Comienza tu día con claridad',
            category: 'meditation',
            difficulty: 'beginner',
            duration: 10,
            demo: true,
          },
        ],
        pagination: { total: 1, page: 1, limit: 10, pages: 1 },
        message: 'Content (DEMO MODE)',
      });
    }

    if (req.path.includes('/sacred-space')) {
      return res.json({
        data: [
          {
            title: 'Santuario de Calma',
            description: 'Un espacio para la tranquilidad interior',
            ambiance: 'calm',
            demo: true,
          },
        ],
        pagination: { total: 1, page: 1, limit: 10, pages: 1 },
        message: 'Sacred spaces (DEMO MODE)',
      });
    }
  }

  next(err);
};

module.exports = demoModeHandler;