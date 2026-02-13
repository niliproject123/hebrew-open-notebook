import { zhCN } from './zh-CN';
import { enUS } from './en-US';
import { zhTW } from './zh-TW';
import { ptBR } from './pt-BR';
import { jaJP } from './ja-JP';
import { itIT } from './it-IT';
import { ruRU } from './ru-RU';
import { heIL } from './he-IL';

export const resources = {
  'zh-CN': { translation: zhCN },
  'en-US': { translation: enUS },
  'zh-TW': { translation: zhTW },
  'pt-BR': { translation: ptBR },
  'ja-JP': { translation: jaJP },
  'it-IT': { translation: itIT },
  'ru-RU': { translation: ruRU },
  'he-IL': { translation: heIL },
} as const;

export type TranslationKeys = typeof enUS;

export type LanguageCode = 'zh-CN' | 'en-US' | 'zh-TW' | 'pt-BR' | 'ja-JP' | 'it-IT' | 'ru-RU' | 'he-IL';

// RTL languages
export const rtlLanguages: LanguageCode[] = ['he-IL'];

export type Language = {
  code: LanguageCode;
  label: string;
};

export const languages: Language[] = [
  { code: 'en-US', label: 'English' },
  { code: 'he-IL', label: 'עברית' },
  { code: 'zh-CN', label: '简体中文' },
  { code: 'zh-TW', label: '繁體中文' },
  { code: 'pt-BR', label: 'Português' },
  { code: 'ja-JP', label: '日本語' },
  { code: 'it-IT', label: 'Italiano' },
  { code: 'ru-RU', label: 'Русский' },
];

export { zhCN, enUS, zhTW, ptBR, jaJP, itIT, ruRU, heIL };
