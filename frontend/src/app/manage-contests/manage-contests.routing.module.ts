import { RouterModule, Routes } from '@angular/router'
import { ManageContestsComponent } from '@/manage-contests/containers/manage-contests/manage-contests.component'
import { NgModule } from '@angular/core'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'manage/contests', component: ManageContestsComponent
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ManageContestsRoutingModule {}