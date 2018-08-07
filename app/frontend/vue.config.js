module.exports = {
  pages: {
    index: {
      // entry for the page
      entry: 'src/pages/index/main.js',
      // the source template
      template: 'public/index.html',
      // output as dist/index.html
      filename: 'index.html'
    },
    about: {
        entry: 'src/pages/about/main.js',
        template: 'public/about.html',
        filename: 'about.html',
        title: 'About Page'
    }
  }
}
