import { Scope, ScopeRecords } from "../../../types/backend/scope";
import { data } from "../types";
import { MixinConstructor } from "./base";

export function ScopeMixin<TBase extends MixinConstructor>(base: TBase) {
    return class ScopeMethods extends base {
        public async own_scopes(): Promise<ScopeRecords> {
            const result = await this.request<ScopeRecords>("/auth/scopes");
            return data(result, {});
        }

        public async all_scopes(): Promise<ScopeRecords> {
            const result = await this.request<ScopeRecords>("/auth/scopes/all");
            return data(result, {});
        }

        public async path_scopes(path: string): Promise<Scope | null> {
            return data(
                await this.request<Scope>(`/auth/scopes/tree/${path}`),
                null
            );
        }

        public async validate_scopes(
            ...scopes: string[]
        ): Promise<{ [key: string]: string[] | null }> {
            return data(
                await this.request<{ [key: string]: string[] }>(
                    "/auth/scopes/validate",
                    { method: "post", body: scopes }
                ),
                scopes.reduce((prev, cur) => ({ ...prev, [cur]: null }), {})
            );
        }
    };
}
