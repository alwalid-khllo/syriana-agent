const { contextBridge, ipcRenderer, webUtils } = require('electron')

contextBridge.exposeInMainWorld('syrianaDesktop', {
  getConnection: profile => ipcRenderer.invoke('syriana:connection', profile),
  revalidateConnection: () => ipcRenderer.invoke('syriana:connection:revalidate'),
  touchBackend: profile => ipcRenderer.invoke('syriana:backend:touch', profile),
  getGatewayWsUrl: profile => ipcRenderer.invoke('syriana:gateway:ws-url', profile),
  openSessionWindow: (sessionId, opts) => ipcRenderer.invoke('syriana:window:openSession', sessionId, opts),
  openNewSessionWindow: () => ipcRenderer.invoke('syriana:window:openNewSession'),
  petOverlay: {
    // Main renderer → main process: window lifecycle + drag. `request` is
    // `{ bounds, screen }`; resolves with the screen bounds it actually used.
    open: request => ipcRenderer.invoke('syriana:pet-overlay:open', request),
    close: () => ipcRenderer.invoke('syriana:pet-overlay:close'),
    setBounds: bounds => ipcRenderer.send('syriana:pet-overlay:set-bounds', bounds),
    setIgnoreMouse: ignore => ipcRenderer.send('syriana:pet-overlay:ignore-mouse', ignore),
    // Flip the overlay focusable (and focus it) while the composer needs keys.
    setFocusable: focusable => ipcRenderer.send('syriana:pet-overlay:set-focusable', focusable),
    // Main renderer → overlay (forwarded by main): push the latest pet state.
    pushState: payload => ipcRenderer.send('syriana:pet-overlay:state', payload),
    // Overlay → main renderer (forwarded by main): pop back in / composer submit.
    control: payload => ipcRenderer.send('syriana:pet-overlay:control', payload),
    // Overlay subscribes to state pushes.
    onState: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('syriana:pet-overlay:state', listener)
      return () => ipcRenderer.removeListener('syriana:pet-overlay:state', listener)
    },
    // Main renderer subscribes to overlay control messages.
    onControl: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('syriana:pet-overlay:control', listener)
      return () => ipcRenderer.removeListener('syriana:pet-overlay:control', listener)
    }
  },
  getBootProgress: () => ipcRenderer.invoke('syriana:boot-progress:get'),
  getConnectionConfig: profile => ipcRenderer.invoke('syriana:connection-config:get', profile),
  saveConnectionConfig: payload => ipcRenderer.invoke('syriana:connection-config:save', payload),
  applyConnectionConfig: payload => ipcRenderer.invoke('syriana:connection-config:apply', payload),
  testConnectionConfig: payload => ipcRenderer.invoke('syriana:connection-config:test', payload),
  probeConnectionConfig: remoteUrl => ipcRenderer.invoke('syriana:connection-config:probe', remoteUrl),
  oauthLoginConnectionConfig: remoteUrl => ipcRenderer.invoke('syriana:connection-config:oauth-login', remoteUrl),
  oauthLogoutConnectionConfig: remoteUrl => ipcRenderer.invoke('syriana:connection-config:oauth-logout', remoteUrl),
  profile: {
    get: () => ipcRenderer.invoke('syriana:profile:get'),
    set: name => ipcRenderer.invoke('syriana:profile:set', name)
  },
  api: request => ipcRenderer.invoke('syriana:api', request),
  notify: payload => ipcRenderer.invoke('syriana:notify', payload),
  requestMicrophoneAccess: () => ipcRenderer.invoke('syriana:requestMicrophoneAccess'),
  readFileDataUrl: filePath => ipcRenderer.invoke('syriana:readFileDataUrl', filePath),
  readFileText: filePath => ipcRenderer.invoke('syriana:readFileText', filePath),
  selectPaths: options => ipcRenderer.invoke('syriana:selectPaths', options),
  writeClipboard: text => ipcRenderer.invoke('syriana:writeClipboard', text),
  saveImageFromUrl: url => ipcRenderer.invoke('syriana:saveImageFromUrl', url),
  saveImageBuffer: (data, ext) => ipcRenderer.invoke('syriana:saveImageBuffer', { data, ext }),
  saveClipboardImage: () => ipcRenderer.invoke('syriana:saveClipboardImage'),
  getPathForFile: file => {
    try {
      return webUtils.getPathForFile(file) || ''
    } catch {
      return ''
    }
  },
  normalizePreviewTarget: (target, baseDir) => ipcRenderer.invoke('syriana:normalizePreviewTarget', target, baseDir),
  watchPreviewFile: url => ipcRenderer.invoke('syriana:watchPreviewFile', url),
  stopPreviewFileWatch: id => ipcRenderer.invoke('syriana:stopPreviewFileWatch', id),
  setTitleBarTheme: payload => ipcRenderer.send('syriana:titlebar-theme', payload),
  setNativeTheme: mode => ipcRenderer.send('syriana:native-theme', mode),
  setTranslucency: payload => ipcRenderer.send('syriana:translucency', payload),
  setPreviewShortcutActive: active => ipcRenderer.send('syriana:previewShortcutActive', Boolean(active)),
  openExternal: url => ipcRenderer.invoke('syriana:openExternal', url),
  openPreviewInBrowser: url => ipcRenderer.invoke('syriana:openPreviewInBrowser', url),
  fetchLinkTitle: url => ipcRenderer.invoke('syriana:fetchLinkTitle', url),
  sanitizeWorkspaceCwd: cwd => ipcRenderer.invoke('syriana:workspace:sanitize', cwd),
  settings: {
    getDefaultProjectDir: () => ipcRenderer.invoke('syriana:setting:defaultProjectDir:get'),
    setDefaultProjectDir: dir => ipcRenderer.invoke('syriana:setting:defaultProjectDir:set', dir),
    pickDefaultProjectDir: () => ipcRenderer.invoke('syriana:setting:defaultProjectDir:pick')
  },
  revealLogs: () => ipcRenderer.invoke('syriana:logs:reveal'),
  getRecentLogs: () => ipcRenderer.invoke('syriana:logs:recent'),
  readDir: dirPath => ipcRenderer.invoke('syriana:fs:readDir', dirPath),
  gitRoot: startPath => ipcRenderer.invoke('syriana:fs:gitRoot', startPath),
  revealPath: targetPath => ipcRenderer.invoke('syriana:fs:reveal', targetPath),
  renamePath: (targetPath, newName) => ipcRenderer.invoke('syriana:fs:rename', targetPath, newName),
  writeTextFile: (filePath, content) => ipcRenderer.invoke('syriana:fs:writeText', filePath, content),
  trashPath: targetPath => ipcRenderer.invoke('syriana:fs:trash', targetPath),
  git: {
    worktreeList: repoPath => ipcRenderer.invoke('syriana:git:worktreeList', repoPath),
    worktreeAdd: (repoPath, options) => ipcRenderer.invoke('syriana:git:worktreeAdd', repoPath, options),
    worktreeRemove: (repoPath, worktreePath, options) =>
      ipcRenderer.invoke('syriana:git:worktreeRemove', repoPath, worktreePath, options),
    branchSwitch: (repoPath, branch) => ipcRenderer.invoke('syriana:git:branchSwitch', repoPath, branch),
    branchList: repoPath => ipcRenderer.invoke('syriana:git:branchList', repoPath),
    repoStatus: repoPath => ipcRenderer.invoke('syriana:git:repoStatus', repoPath),
    fileDiff: (repoPath, filePath) => ipcRenderer.invoke('syriana:git:fileDiff', repoPath, filePath),
    scanRepos: (roots, options) => ipcRenderer.invoke('syriana:git:scanRepos', roots, options),
    review: {
      list: (repoPath, scope, baseRef) => ipcRenderer.invoke('syriana:git:review:list', repoPath, scope, baseRef),
      diff: (repoPath, filePath, scope, baseRef, staged) =>
        ipcRenderer.invoke('syriana:git:review:diff', repoPath, filePath, scope, baseRef, staged),
      stage: (repoPath, filePath) => ipcRenderer.invoke('syriana:git:review:stage', repoPath, filePath),
      unstage: (repoPath, filePath) => ipcRenderer.invoke('syriana:git:review:unstage', repoPath, filePath),
      revert: (repoPath, filePath) => ipcRenderer.invoke('syriana:git:review:revert', repoPath, filePath),
      revParse: (repoPath, ref) => ipcRenderer.invoke('syriana:git:review:revParse', repoPath, ref),
      commit: (repoPath, message, push) => ipcRenderer.invoke('syriana:git:review:commit', repoPath, message, push),
      commitContext: repoPath => ipcRenderer.invoke('syriana:git:review:commitContext', repoPath),
      push: repoPath => ipcRenderer.invoke('syriana:git:review:push', repoPath),
      shipInfo: repoPath => ipcRenderer.invoke('syriana:git:review:shipInfo', repoPath),
      createPr: repoPath => ipcRenderer.invoke('syriana:git:review:createPr', repoPath)
    }
  },
  terminal: {
    dispose: id => ipcRenderer.invoke('syriana:terminal:dispose', id),
    resize: (id, size) => ipcRenderer.invoke('syriana:terminal:resize', id, size),
    start: options => ipcRenderer.invoke('syriana:terminal:start', options),
    write: (id, data) => ipcRenderer.invoke('syriana:terminal:write', id, data),
    onData: (id, callback) => {
      const channel = `syriana:terminal:${id}:data`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    },
    onExit: (id, callback) => {
      const channel = `syriana:terminal:${id}:exit`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    }
  },
  onClosePreviewRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('syriana:close-preview-requested', listener)
    return () => ipcRenderer.removeListener('syriana:close-preview-requested', listener)
  },
  onOpenUpdatesRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('syriana:open-updates', listener)
    return () => ipcRenderer.removeListener('syriana:open-updates', listener)
  },
  onDeepLink: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:deep-link', listener)
    return () => ipcRenderer.removeListener('syriana:deep-link', listener)
  },
  signalDeepLinkReady: () => ipcRenderer.invoke('syriana:deep-link-ready'),
  onWindowStateChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:window-state-changed', listener)
    return () => ipcRenderer.removeListener('syriana:window-state-changed', listener)
  },
  onFocusSession: callback => {
    const listener = (_event, sessionId) => callback(sessionId)
    ipcRenderer.on('syriana:focus-session', listener)
    return () => ipcRenderer.removeListener('syriana:focus-session', listener)
  },
  onNotificationAction: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:notification-action', listener)
    return () => ipcRenderer.removeListener('syriana:notification-action', listener)
  },
  onPreviewFileChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:preview-file-changed', listener)
    return () => ipcRenderer.removeListener('syriana:preview-file-changed', listener)
  },
  onBackendExit: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:backend-exit', listener)
    return () => ipcRenderer.removeListener('syriana:backend-exit', listener)
  },
  onPowerResume: callback => {
    const listener = () => callback()
    ipcRenderer.on('syriana:power-resume', listener)
    return () => ipcRenderer.removeListener('syriana:power-resume', listener)
  },
  onBootProgress: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:boot-progress', listener)
    return () => ipcRenderer.removeListener('syriana:boot-progress', listener)
  },
  // First-launch bootstrap progress -- emitted by the install.ps1 stage
  // runner in main.cjs (apps/desktop/electron/bootstrap-runner.cjs).
  // Renderer's install overlay subscribes to live events and queries the
  // current snapshot via getBootstrapState() to recover after a devtools
  // reload mid-bootstrap.
  getBootstrapState: () => ipcRenderer.invoke('syriana:bootstrap:get'),
  resetBootstrap: () => ipcRenderer.invoke('syriana:bootstrap:reset'),
  repairBootstrap: () => ipcRenderer.invoke('syriana:bootstrap:repair'),
  cancelBootstrap: () => ipcRenderer.invoke('syriana:bootstrap:cancel'),
  onBootstrapEvent: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('syriana:bootstrap:event', listener)
    return () => ipcRenderer.removeListener('syriana:bootstrap:event', listener)
  },
  getVersion: () => ipcRenderer.invoke('syriana:version'),
  getRemoteDisplayReason: () => ipcRenderer.invoke('syriana:get-remote-display-reason'),
  uninstall: {
    summary: () => ipcRenderer.invoke('syriana:uninstall:summary'),
    run: mode => ipcRenderer.invoke('syriana:uninstall:run', { mode })
  },
  updates: {
    check: () => ipcRenderer.invoke('syriana:updates:check'),
    apply: opts => ipcRenderer.invoke('syriana:updates:apply', opts),
    getBranch: () => ipcRenderer.invoke('syriana:updates:branch:get'),
    setBranch: name => ipcRenderer.invoke('syriana:updates:branch:set', name),
    onProgress: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('syriana:updates:progress', listener)
      return () => ipcRenderer.removeListener('syriana:updates:progress', listener)
    }
  },
  themes: {
    fetchMarketplace: id => ipcRenderer.invoke('syriana:vscode-theme:fetch', id),
    searchMarketplace: query => ipcRenderer.invoke('syriana:vscode-theme:search', query)
  }
})
