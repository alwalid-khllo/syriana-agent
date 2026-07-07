import { useQuery } from '@tanstack/react-query'

import { getSyrianaConfigRecord } from '@/syriana'
import { queryClient, writeCache } from '@/lib/query-client'
import type { SyrianaConfigRecord } from '@/types/syriana'

// One shared cache for the whole profile config record (`GET /api/config`).
// Every settings surface (MCP, model, config) reads and writes through this key
// so a save in one shows in the others, and revisiting a tab paints the cache
// instead of blanking on a fresh fetch.
//
// Distinct from session/hooks/use-syriana-config.ts, which is side-effecting —
// it pushes personality/cwd/voice/… into the session stores for live chat.
export const SYRIANA_CONFIG_KEY = ['syriana-config-record'] as const

// staleTime 0 → serve cache instantly, background-revalidate on every mount.
export const useSyrianaConfigRecord = () =>
  useQuery({ queryKey: SYRIANA_CONFIG_KEY, queryFn: getSyrianaConfigRecord, staleTime: 0 })

export const setSyrianaConfigCache = writeCache<SyrianaConfigRecord>(SYRIANA_CONFIG_KEY)

export const invalidateSyrianaConfig = () => queryClient.invalidateQueries({ queryKey: SYRIANA_CONFIG_KEY })
