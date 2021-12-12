import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { COMPONENTS, ContestsRoutingModule } from '@/contests/contests.routing.module'
import { ContestsStore } from '@/contests/contests.store'
import { AgGridModule } from 'ag-grid-angular'


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        AgGridModule,
        ContestsRoutingModule
    ],
    providers: [
        { provide: ContestsStore }
    ]
} )
export class ContestsModule {}