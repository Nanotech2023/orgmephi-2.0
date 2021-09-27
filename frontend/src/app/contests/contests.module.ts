import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { COMPONENTS, ContestsRoutingModule } from '@/contests/contests.routing.module'
import { ContestsStore } from '@/contests/contests.store'


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        ContestsRoutingModule
    ],
    providers: [
        { provide: ContestsStore }
    ]
} )
export class ContestsModule {}