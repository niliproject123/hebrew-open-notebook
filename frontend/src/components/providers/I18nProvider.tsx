'use client'

import React, { useEffect, useState } from 'react'
import i18n from '@/lib/i18n'
import { LanguageLoadingOverlay } from '@/components/common/LanguageLoadingOverlay'
import { rtlLanguages, LanguageCode } from '@/lib/locales'

function updateDocumentDirection(language: string) {
  const isRtl = rtlLanguages.includes(language as LanguageCode)
  document.documentElement.dir = isRtl ? 'rtl' : 'ltr'
  document.documentElement.lang = language
}

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)

    // Set initial direction based on current language
    updateDocumentDirection(i18n.language)

    // Listen for language changes
    const handleLanguageChange = (lng: string) => {
      updateDocumentDirection(lng)
    }

    i18n.on('languageChanged', handleLanguageChange)

    return () => {
      i18n.off('languageChanged', handleLanguageChange)
    }
  }, [])

  // Avoid hydration mismatch by waiting for mount
  if (!mounted) {
    return <div style={{ visibility: 'hidden' }}>{children}</div>
  }

  return (
    <>
      <LanguageLoadingOverlay />
      {children}
    </>
  )
}
