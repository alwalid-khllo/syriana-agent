import { getGlobalModelOptions, type SyrianaGateway, type ModelOptionsResponse } from '@/syriana'

interface ModelOptionsRequest {
  gateway?: SyrianaGateway
  refresh?: boolean
  sessionId?: null | string
}

export function requestModelOptions({
  gateway,
  refresh = false,
  sessionId
}: ModelOptionsRequest): Promise<ModelOptionsResponse> {
  if (gateway) {
    const params: Record<string, unknown> = {}

    if (sessionId) {
      params.session_id = sessionId
    }

    if (refresh) {
      params.refresh = true
    }

    return gateway.request<ModelOptionsResponse>('model.options', params)
  }

  return getGlobalModelOptions(refresh ? { refresh: true } : undefined)
}
