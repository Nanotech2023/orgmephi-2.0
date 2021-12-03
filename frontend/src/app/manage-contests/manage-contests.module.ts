import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { COMPONENTS, ManageContestsRoutingModule } from '@/manage-contests/manage-contests.routing.module'
import { DxDataGridModule, DxSpeedDialActionModule } from 'devextreme-angular'


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        DxDataGridModule,
        DxSpeedDialActionModule,
        ManageContestsRoutingModule
    ]
} )
export class ManageContestsModule {}